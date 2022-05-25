"""Contains scheduler optimization algorithms."""
from collections import queue
from datetime import datetime

from .types import AlgorithmType
from .types import PhysCostCallableType
from .types import TaskListType
from maweid.task import TaskData


def optimize_fifo(
    tasks: TaskListType, current_time: datetime, task_cost: PhysCostCallableType
) -> queue.Queue[TaskData]:
    """Optimize the tasks in FIFO order.

    Args:
        tasks: List of tasks to optimize.
        current_time: Current time of the timeline.
        task_cost: Callable that computes the physical cost of a task.

    Returns:
        A queue of tasks in FIFO order.

    """
    q = queue.Queue()
    for task in tasks:
        q.put(task)
    return q


_algorithms = {
    "FIFO": optimize_fifo,
}


def add_algorithm(name: str, func: AlgorithmType) -> None:
    """Add an algorithm to the list of available algorithms."""
    if name in _algorithms:
        raise ValueError(f"Algorithm {name} already exists.")
    _algorithms[name] = func


def get_algorithm(name: str):
    """Get an algorithm from the list of available algorithms."""
    if name not in _algorithms:
        raise ValueError(f"Algorithm {name} does not exist.")
    return _algorithms[name]
