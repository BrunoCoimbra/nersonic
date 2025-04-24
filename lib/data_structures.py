from dataclasses import dataclass, field


@dataclass
class Job:
    """
    A class representing a batch job.
    """

    id: str
    array_id: str
    state: str
    worker_node: str


class JobArray(list):
    """
    A class representing a batch job array.
    """

    def __init__(self, *args, id: str = None):
        super().__init__(*args)
        self.id = id


class JobQueue(dict):
    """
    A class representing a job queue.
    """
