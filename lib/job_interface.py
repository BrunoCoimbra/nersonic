import json
from time import sleep
from typing import Protocol

from lib.api_client import ApiClient, ConfigManager

config = ConfigManager()


class JobInterface(Protocol):
    """
    Interface for job classes.
    """

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def submit(self, job: str) -> str:
        """
        Submits a job to the NERSC API.

        Args:
            job (str): The job to be submitted.
        Returns:
            str: The job ID of the submitted job.
        """

    def cancel(self, job_id: str) -> bool:
        """
        Cancels a job on the NERSC API.

        Args:
            job_id (str): The ID of the job to be canceled.
        Returns:
            bool: True if the job was canceled successfully, False otherwise.
        """

    def status(self, job_id: str) -> str:
        """
        Gets the status of a job on the NERSC API.

        Args:
            job_id (str): The ID of the job to check.
        Returns:
            str: The status of the job.
        """

    def queue(self) -> list:
        """
        Gets the list of jobs in the queue on the NERSC API.

        Returns:
            list: A list of jobs in the queue.
        """


class NerscJobInterface(JobInterface):
    """
    NERSC job interface class.
    """

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)
        self.machine = config.get("NERSC", "Machine")

    def submit(self, job):
        data = {
            "job": job,
            "isPath": False,
        }

        response = self.api_client.request(
            "POST", f"/compute/jobs/{self.machine}", data=data)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to submit job: {response.text}")
        task_id = response.json().get("task_id")

        timeout = int(config.get("GENERAL", "ApiRequestTimeout"))
        while True:
            response = self.api_client.request("GET", f"/tasks/{task_id}")
            task_status = response.json().get("status")
            if task_status == "completed":
                break
            sleep(1)
            timeout -= 1
            if timeout <= 0:
                raise TimeoutError(
                    f"Timeout waiting for task {task_id} to complete.")
        task_result = json.loads(response.json().get("result"))

        if task_result.get("status") != "ok":
            raise RuntimeError(f"Failed to submit job: {task_result}")

        return task_result.get("jobid")

    def cancel(self, job_id):
        response = self.api_client.request(
            "DELETE", f"/compute/jobs/{self.machine}/{job_id}")
        return response.status_code == 200

    def status(self, job_id):
        response = self.api_client.request(
            "GET", f"/compute/jobs/{self.machine}/{job_id}")
        return response.json()

    def queue(self):
        params = {
            "cached": "false",
            "kwargs": f"user={config.get("GENERAL", "UserName")}"
        }

        response = self.api_client.request(
            "GET", f"/compute/jobs/{self.machine}", params=params)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to get job queue: {response.text}")

        return response.json().get("output")
