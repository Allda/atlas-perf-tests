import os
import uuid

from locust import HttpUser, between, task

from client import CLIENT


class BombasticTasks(HttpUser):
    wait_time = between(1, 2)
    host = os.environ.get("BOMASTIC_HOST", "https://sbom.atlas.stage.devshift.net")

    test_sbom = "perf-test-container-1.3"

    def on_start(self):
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
        Perform a GET request to retrieve a SBOM
        """

        self.client.get(
            "/api/v1/sbom",
            params={"id": self.test_sbom},
        )

    @task
    def upload_sbom(self) -> None:
        """
        Perform a PUT request to upload a SBOM and then delete it
        """
        with open("data/test_sbom_perf_test.json", "rb") as f:
            sbom = f.read()
        sbom_id = str(uuid.uuid4())
        self.client.put(
            "/api/v1/sbom",
            params={"id": sbom_id},
            data=sbom,
            headers={"Content-Type": "application/json"},
            name="/api/v1/sbom",
        )
        self.client.delete(f"/api/v1/sbom", params={"id": sbom_id}, name="/api/v1/sbom")

    @task
    def search(self) -> None:
        """
        Perform a GET request to search for a SBOM
        """
        self.client.get(
            "/api/v1/sbom/search",
            params={"q": self.test_sbom},
        )
