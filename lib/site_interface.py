from typing import Protocol
from lib.data_structures import JobArray, JobDictionary


class SiteInterface(Protocol):
    """
    Interface for job classes.
    """

    async def run(self, executable_path, args: list = None) -> str:
        """
        Runs a command on the site.

        Args:
            executable_path (str): The path to the executable.
            args (list): The arguments to pass to the executable.
        Returns:
            str: The output of the command.
        """

    async def upload(self, file_path: str) -> str:
        """
        Uploads a file to the site.

        Args:
            file_path (str): The path to the file to be uploaded.
        Returns:
            str: The path of the uploaded file on the site.
        """

    async def submit_job(self, job_path: str) -> str:
        """
        Submits a job to the site.

        Args:
            job_path (str): The job to be submitted.
        Returns:
            str: The ID of the submitted job array.
        """

    async def cancel_job(self, job_id: str):
        """
        Cancels a job on the site.

        Args:
            job_id (str): The ID of the job to be canceled.
        Returns:
            bool: True if the job was canceled successfully, False otherwise.
        """

    async def job_status(self, job_id: str) -> JobArray:
        """
        Gets the status of a job on the site.

        Args:
            job_id (str): The ID of the job to check.
        Returns:
            JobArray: The status of the job.
        """

    async def job_history(self, job_id: str) -> JobArray:
        """
        Gets the history of a job on the site.

        Args:
            job_id (str): The ID of the job to check.
        Returns:
            JobArray: The history of the job.
        """

    async def queue(self) -> JobDictionary:
        """
        Gets the list of jobs in the queue on the site.

        Returns:
            JobQueue: Jobs in the queue grouped by job array.
        """

    async def history(self) -> JobDictionary:
        """
        Gets the list of jobs in the history on the site.

        Returns:
            JobQueue: Jobs in the history grouped by job array.
        """
