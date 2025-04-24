from time import sleep

from lib.api_client import NerscApiClient
from lib.job_interface import NerscJobInterface
from lib.job_manager import JobManager

with open("./sample_jobs/test.sh", "r") as f:
    JOB = f.read()


def main():
    print("NERSC Triton Test")
    print("-----------------\n")

    print("Connecting to NERSC API...")
    client = NerscApiClient()
    client.connect()
    if not client.connected:
        print("Failed to connect to NERSC API.")
        return
    print("Connected to NERSC API.\n")

    job_manager = JobManager(NerscJobInterface(client))

    print("Submitting job Triton Server job...")
    job_manager.submit(name="triton-server", job_path="/workspaces/nersonic/slurm_triton_deployment/start_triton_slurm.sh")
    print("Done submitting job.\n")

    print("Waiting for job to start...")
    while True:
        job_manager.update_queue()
        job = job_manager.get(name="triton-server")[0]
        if job.state == "RUNNING":
            print("Job started successfully.")
            break
        elif job.state == "FAILED":
            print("Job failed to start.")
            return
        elif job.state == "CANCELLED":
            print("Job was cancelled.")
            return
        else:
            print(f"Job {job.id} status: {job.state} - sleeping for 60 seconds...")
        sleep(60)

if __name__ == "__main__":
    main()
