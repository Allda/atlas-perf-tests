import os
import time
from typing import Any

import requests

from client import CLIENT

BOMASTIC_HOST = os.environ.get("BOMASTIC_HOST", "https://sbom.atlas.stage.devshift.net")
VEXINATION_HOST = os.environ.get(
    "VEXINATION_HOST", "https://vex.atlas.stage.devshift.net"
)


def wait_for_search(session: Any, url: str, query: dict[str, str]) -> None:
    """
    Wait for a search to be available on the given URL with the given query

    Args:
        session (Any): Session to use for the requests
        url (str): API URL to use for the search
        query (dict[str, str]): API query to use for the search
    """
    search_available = False
    print(f"Waiting for search to be available: {query}")
    while search_available is False:
        resp = session.get(url, params=query)
        if resp.ok:
            total = resp.json().get("total", 0)
            print("Found total:", total)
            if resp.json().get("total", 0) > 0:
                search_available = True
                print(f"Search available: {query}")
        if search_available is False:
            time.sleep(5)


def init_data() -> None:
    """
    Initialize the data for the performance tests and wait for it to be available
    """
    session = requests.Session()
    CLIENT.ensure_valid_token()
    session.headers["Authorization"] = "Bearer " + CLIENT._token

    sbom_id = "perf-test-container-1.3"
    with open("data/test_sbom_perf_test.json", "rb") as f:
        sbom = f.read()
        resp = session.put(
            f"{BOMASTIC_HOST}/api/v1/sbom",
            params={"id": sbom_id},
            data=sbom,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()

    print(f"SBOM uploaded successfully: {sbom_id}")

    vex_id = "CVE-1990-1111"
    with open("data/CVE-1990-1111.json", "rb") as f:
        sbom = f.read()
        resp = session.put(
            f"{VEXINATION_HOST}/api/v1/vex",
            params={"advisory": vex_id},
            data=sbom,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()

    print(f"VEX uploaded successfully: {vex_id}")

    wait_for_search(session, f"{BOMASTIC_HOST}/api/v1/sbom/search", {"q": sbom_id})
    wait_for_search(session, f"{VEXINATION_HOST}/api/v1/vex/search", {"q": vex_id})


def main() -> None:
    """
    Main function
    """
    init_data()


if __name__ == "__main__":
    main()
