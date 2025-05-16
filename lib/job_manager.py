import asyncio

from lib.data_structures import JobArray, JobDictionary
from lib.site_interface import SiteInterface


class JobManager:
    def __init__(self, site_interface: SiteInterface):
        self.site_interface = site_interface
        self.queue = JobDictionary()
        self.name_to_job_id = {}

    def get(self, name: str = None, job_id: str = None) -> JobArray:
        """
        Gets the status of a job from the job manager queue.

        Args:
            name (str): The name of the job.
            job_id (str): The ID of the job.
        Returns:
            str: The status of the job.
        """

        if name:
            job_id = self.name_to_job_id.get(name)
        
        if job_id not in self.queue:
            raise ValueError(f"Job ID {job_id} not found in the job manager.")

        return self.queue[job_id]

    def submit(self, name: str = None, job_path: str = None) -> str:
        """
        Submits a job to the site.

        Args:
            name (str): The name of the job.
            job_path (str): The path to the job file.
        Returns:
            str: The ID of the submitted job array.
        """

        if job_path is None:
            raise ValueError("job_path must be provided.")
        
        job_id = asyncio.run(self.site_interface.submit_job(job_path))
        job_status = asyncio.run(self.site_interface.job_status(job_id))
        self.queue[job_id] = job_status
        if name:
            self.name_to_job_id[name] = job_id

        return job_id
    
    def cancel(self, name: str = None, job_id: str = None):
        """
        Cancels a job on the site.

        Args:
            name (str): The name of the job to be canceled.
            job_id (str): The ID of the job to be canceled. ("all" to cancel all jobs)
        Returns:
            bool: True if the job was canceled successfully, False otherwise.
        """

        if job_id == "all":
            job_list = list(self.queue.keys())
        else:
            if name:
                job_list = [self.name_to_job_id.get(name)]
            if job_id not in self.queue:
                raise ValueError(f"Job ID {job_id} not found in the job manager.")
        
        async def runner():
            await asyncio.gather(
                *[self.site_interface.cancel_job(job_id) for job_id in job_list]
            )

        asyncio.run(runner())

    def update_queue(self):
        """
        Updates the status of all jobs in the job manager.
        """

        async def runner():
            return await asyncio.gather(
                self.site_interface.queue(),
                self.site_interface.history()
            )
        queue, history = asyncio.run(runner())

        for job_id in self.queue:
            if job_id in queue:
                self.queue[job_id] = queue[job_id]
            elif job_id in history:
                self.queue[job_id] = history[job_id]


    def load(self, name: str = None, job_id: str = None):
        """
        Loads the status of a job from the batch system into the job manager queue.

        Args:
            name (str): The name of the job to be loaded.
            job_id (str): The ID of the job to be loaded. ("all" to load all jobs)
        Returns:
            JobDictionary: The status of the job.
        """

        if job_id == "all":
            queue = asyncio.run(self.site_interface.queue())
            self.queue.update(queue)
            return
        
        job_status = self.site_interface.status(job_id)
        self.queue[job_id] = job_status
        if name:
            self.name_to_job_id[name] = job_id
