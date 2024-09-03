"""
This module provides a client for the OpenID Connect client credentials flow.
"""
import os

from auth import OIDCClientCredentials, OIDCClientCredentialsClient

CLIENT = OIDCClientCredentialsClient(
    OIDCClientCredentials(
        os.environ["TOKEN_URL"],
        os.environ["CLIENT_ID"],
        os.environ["CLIENT_SECRET"],
    )
)
