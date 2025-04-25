from lib.data_structures import JobDictionary, JobArray
from lib.job_interface import JobInterface


class JobManager:
    def __init__(self, job_interface: JobInterface):
        self.job_interface = job_interface
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

    def submit(self, name: str = None, job: str = None, job_path: str = None) -> str:
        """
        Submits a job to the NERSC API.

        Args:
            name (str): The name of the job.
            job (str): The job to be submitted.
            job_path (str): The path to the job file.
        Returns:
            str: The ID of the submitted job array.
        """

        if job is None and job_path is None:
            raise ValueError("Either job or job_path must be provided.")
        if job_path is not None:
            with open(job_path, "r") as f:
                job = f.read()
        
        job_id = self.job_interface.submit_job(job)
        job_status = self.job_interface.job_status(job_id)
        self.queue[job_id] = job_status
        if name:
            self.name_to_job_id[name] = job_id

        return job_id
    
    def cancel(self, name: str = None, job_id: str = None) -> bool:
        """
        Cancels a job on the NERSC API.

        Args:
            name (str): The name of the job to be canceled.
            job_id (str): The ID of the job to be canceled. ("all" to cancel all jobs)
        Returns:
            bool: True if the job was canceled successfully, False otherwise.
        """

        if job_id == "all":
            success = True
            for job in self.queue:
                success = self.job_interface.cancel(job) and success
            return success

        if name:
            job_id = self.name_to_job_id.get(name)

        if job_id not in self.queue:
            raise ValueError(f"Job ID {job_id} not found in the job manager.")

        return self.job_interface.cancel(job_id)

    def update_queue(self):
        """
        Updates the status of all jobs in the job manager.
        """

        queue = self.job_interface.queue()
        history = self.job_interface.history()
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
            queue = self.job_interface.queue()
            self.queue.update(queue)
            return
        
        job_status = self.job_interface.status(job_id)
        self.queue[job_id] = job_status
        if name:
            self.name_to_job_id[name] = job_id
