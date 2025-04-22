from lib.api_client import NerscApiClient
from lib.job_interface import NerscJobInterface

with open("./sample_jobs/test.sh", "r") as f:
    JOB = f.read()


def main():
    print("Hello from nersonic!")

    client = NerscApiClient()
    client.connect()
    job_interface = NerscJobInterface(client)

    job_id = job_interface.submit(JOB)
    status = job_interface.status(job_id)
    queue = job_interface.queue()


if __name__ == "__main__":
    main()
