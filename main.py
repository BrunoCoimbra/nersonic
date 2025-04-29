import os
import subprocess

from time import sleep

from lib.nersc_site_interface import NerscSiteInterface
from lib.job_manager import JobManager

from configparser import ConfigParser


def main():
    print("NERSC Triton Test")
    print("-----------------\n")

    job_manager = JobManager(NerscSiteInterface(config["NERSC"]))

    print("Submitting job Triton Server job...")
    job_manager.submit(name="triton-server", job_path=f"{ROOT_DIR}/sample_jobs/test.sh")
    print("Done submitting job.\n")

    print("Waiting for job to start...")
    while True:
        job_manager.update_queue()
        job = job_manager.get(name="triton-server")[0]
        print(f"Job ID: {job.id}, State: {job.state}")
        if job.state != "PENDING":
            break
        print("Sleeping for 60 seconds...")
        sleep(60)

    print("Starting load balancer...")
    try:
        lb = subprocess.Popen(f"{ROOT_DIR}/slurm_triton_deployment/start_lb.sh {job.id}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while lb.poll() is None:
            output = lb.stdout.readline()
            if output == b"" and lb.poll() is not None:
                break
            if output:
                print(output.decode().strip())
        print("Load balancer exited with code:", lb.poll())
        print(lb.stdout.read().decode())
        print(lb.stderr.read().decode())
    except KeyboardInterrupt:
        print("Stopping load balancer...")
        lb.terminate()
        lb.wait()
        print("Load balancer terminated.\n")
        print("Exiting...")

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    config = ConfigParser()
    config.read(os.path.join(ROOT_DIR, "settings.cfg"))

    main()
