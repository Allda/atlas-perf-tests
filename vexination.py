import os

from locust import HttpUser, between, task

from client import CLIENT


class VexinationTasks(HttpUser):
    wait_time = between(1, 2)
    host = os.environ.get("VEXINATION_HOST", "https://vex.atlas.stage.devshift.net")
    vex_id = "CVE-1990-1111"

    def on_start(self) -> None:
        """
        Set the Authorization header to the token
        """
        self.client.headers["Authorization"] = "Bearer " + self.login()

    def login(self) -> str:
        """
        Login to the service and return the token

        Returns:
            str: Access token
        """
        global CLIENT
        CLIENT.ensure_valid_token()
        return CLIENT._token

    @task
    def get_sbom(self) -> None:
        """
        Perform a GET request to retrieve a VEX
        """
        self.client.get("/api/v1/vex", params={"advisory": self.vex_id})

    @task
    def search(self) -> None:
        """
        Perform a GET request to search for a VEX
        """
        self.client.get(
            "/api/v1/vex/search",
            params={"q": self.vex_id},
        )
