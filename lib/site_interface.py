from typing import Protocol
from lib.data_structures import JobArray, JobDictionary


class SiteInterface(Protocol):
    """
    Interface for job classes.
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
