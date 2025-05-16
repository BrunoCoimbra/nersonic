import os
import subprocess

from time import sleep

from lib.nersc_site_interface import NerscSiteInterface
from lib.job_manager import JobManager
from lib.process_manager import ProcessManager

from configparser import ConfigParser


def main():
    print("NERSC Triton Test")
    print("-----------------\n")

    site_interface = NerscSiteInterface(config["NERSC"])
    job_manager = JobManager(site_interface)
    process_manager = ProcessManager(site_interface, config["GENERAL"])

    print("Submitting job Triton Server job...")
    job_manager.submit(name="triton-server", job_path=f"{ROOT_DIR}/scripts/start_triton_slurm.sh")
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

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    config = ConfigParser()
    config.read(os.path.join(ROOT_DIR, "settings.cfg"))

    main()
