import os
import json

from io import BytesIO

from sfapi_client import AsyncClient
from sfapi_client.compute import Machine
from sfapi_client.jobs import JobCommand

from authlib.jose import JsonWebKey

from lib.data_structures import Job, JobArray, JobDictionary
from lib.site_interface import SiteInterface

class NerscSiteInterface(SiteInterface):
    """
    NERSC job interface class.
    """

    def __init__(self, config):
        self.user = config.get("UserName")
        with open(config.get("ClientIdPath"), "r") as f:
            self.client_id = f.read()
        with open(config.get("PrivateKeyPath")) as f:
            self.secret = JsonWebKey.import_key(json.loads(f.read()))
        self.transfer_dir = config.get("TransferDir")

    async def submit_job(self, job_path) -> str:
        async with AsyncClient(self.client_id, self.secret) as client:
            compute = await client.compute(Machine.perlmutter)

            [path] = await compute.ls(self.transfer_dir, directory=True)
            with open(job_path, "rb") as f:
                job_file = BytesIO(f.read())
                job_file.filename = os.path.basename(job_path)
                await path.upload(job_file)

            job = await compute.submit_job(os.path.join(str(path), job_file.filename))

        return job.jobid

    async def cancel_job(self, job_id):
        async with AsyncClient(self.client_id, self.secret) as client:
            compute = await client.compute(Machine.perlmutter)

        job = await compute.job(job_id)
        await job.cancel()

    async def job_status(self, job_id: str) -> JobArray:
        queue = await self.queue()
        return queue[job_id]
    
    async def job_history(self, job_id: str) -> JobArray:
        history = await self.history()
        return history[job_id]

    async def queue(self, history=False) -> JobDictionary:
        async with AsyncClient(self.client_id, self.secret) as client:
            compute = await client.compute(Machine.perlmutter)
            jobs = await compute.jobs(user=self.user)

        job_queue = JobDictionary()
        for job in jobs:
            job_array = job_queue.setdefault(
                job.array_job_id,
                JobArray(id=job.array_job_id)
            )
            job_array.append(Job(
                id=job.jobid,
                array_id=job.array_job_id,
                state=job.state.name,
                worker_node=job.exec_host
            ))
            
        return job_queue

    async def history(self):
        async with AsyncClient(self.client_id, self.secret) as client:
            compute = await client.compute(Machine.perlmutter)
            jobs = await compute.jobs(user=self.user, command=JobCommand.sacct)

        job_history = JobDictionary()
        for job in jobs:
            array_id = job.jobid.split("_")[0]
            job_array = job_history.setdefault(
                array_id,
                JobArray(id=array_id)
            )
            job_array.append(Job(
                id=job.jobidraw,
                array_id=array_id,
                state=job.state.name,
                worker_node=job.nodelist
            ))
            
        return job_history
