"""
OIDC client credential flow
"""

import logging
import time
from dataclasses import dataclass
from threading import Lock

import requests

LOGGER = logging.getLogger(__name__)


class OIDCAuthenticationError(Exception):
    """
    Raised when token refresh fails
    """


@dataclass
class OIDCClientCredentials:
    """
    Container class for the authentication info necessary for the OIDC
    client credential flow

    Fields:
        token_url (str): The OAuth2/OIDC token endpoint. Can usually be obtained
            by fetching ${oidc_root}/.well-known/openid-configuration and extracting
            the token_endpoint field
        client_id (str): Client ID to be used to obtain a JWT token
        client_secret (str): Client secret to be used to obtain a JWT token
    """

    token_url: str
    client_id: str
    client_secret: str


class OIDCClientCredentialsClient:
    """
    Generic OIDC client credential client

    Transparently handles the OIDC client credential flow required for authentication,
    including automatic token renewal.
    """

    def __init__(
        self,
        auth: OIDCClientCredentials,
    ):
        """
        Create a new client

        Args:
            auth (OIDCClientCredentials): Authentication info
            proxy (Optional[str]): Proxy to use to talk to the API server
                Defaults to None, which means no proxy.
        """
        self._auth = auth
        self._token = ""
        self._token_expiration = 0
        self._token_mutex = Lock()

    def _token_expired(self) -> bool:
        """
        Check if the current token should be renewed

        Returns:
            bool: True if the current token needs to be renewed
        """
        # Avoid reusing a token which is too close to its expiration by considering it
        # expired if it has less than 15 seconds of validity left
        return time.time() > self._token_expiration - 15

    def _fetch_token(self) -> None:
        """
        Retrieve a new token using the OAuth2/OID client credential flow

        Raises:
            OIDCAuthenticationError: If the token renewal failed
        """
        # See https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/
        # and https://www.ietf.org/rfc/rfc6749.txt section 4.4 and 2.3.1
        LOGGER.debug("Fetching new token from %s", self._auth.token_url)
        resp = requests.post(
            self._auth.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self._auth.client_id,
                "client_secret": self._auth.client_secret,
            },
            timeout=60,
        )
        if not resp.ok:
            LOGGER.error(
                "Unable to fetch auth token. [%s] %s", resp.status_code, resp.text
            )
            resp.raise_for_status()
        token = resp.json()
        if "access_token" not in token:
            if "error" in token:
                error_type = token["error"]
                error_description = token.get("error_description", "")
                error_msg = f"Authentication failed: {error_type} {error_description}"
            else:
                error_msg = "Authentication server did not provide a token"
            raise OIDCAuthenticationError(error_msg)
        self._token = token["access_token"]
        self._token_expiration = int(token.get("expires_in", 300) + time.time())
        return self._token

    def ensure_valid_token(self) -> None:
        """
        Check if we have a valid token and if not, renew it
        """
        with self._token_mutex:
            if self._token_expired():
                self._fetch_token()
