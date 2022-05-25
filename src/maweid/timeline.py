"""Module containing classes and functions relating to building a timeline."""
import typing as t
from abc import ABC
from collections import queue
from dataclasses import dataclass
from datetime import datetime

from .task import Task
from .task import TaskStatus
from .types import TaskListType
from maweid.optimization import get_algorithm


@dataclass
class TimelinePhysicalState(ABC):
    """Represents the physical state of the timeline."""

    pass


class TaskInTimeline:
    """Hold task in timeline."""

    task: Task
    predicted_start_time: datetime = None


class Timeline:
    """Class representing a timeline that inserts tasks."""

    def __init__(
        self,
        start_date: datetime,
        algorithm: str,
        on_task_change: t.Callable[[Task], None],
    ):
        """Initializes the timeline."""
        self.timeline: queue.Queue[TaskInTimeline] = queue.Queue()
        self.current_time: datetime = start_date
        self.start_date: datetime = start_date
        self.tasks: t.Dict[TaskInTimeline] = {}
        self.completed_tasks: TaskListType = []
        self.cancelled_tasks: TaskListType = []
        self.error_tasks: TaskListType = []
        self.algorithm = get_algorithm(algorithm)
        self.current_task: Task = None
        self.physical_state = None
        self.on_task_change = on_task_change

    def update_time(self):
        """Updates the current time. Implement to update the current time."""
        raise NotImplementedError

    def update_physical_state(self):
        """Updates the physical state of the timeline."""
        pass

    # TODO: Figure out more comprehensive way to handle this
    def compute_physical_cost(self, task: Task):
        """Computes the physical cost of the task.

        For example if it takes a long time to move from one task to another that
        may be physically distant
        """
        return 0.0

    # Check to make sure task is unique
    def insert_task(self, task: Task):
        """Inserts a task into the timeline."""
        if task.task_id in self.tasks:
            raise ValueError(f"Task {task} already exists.")
        self.tasks[task.task_id] = task
        self.optimize()

    def bulk_insert_task(self, tasks: t.List[Task]):
        """Inserts a task into the timeline."""
        for task in tasks:
            if task.task_id in self.tasks:
                raise ValueError(f"Task {task} already exists.")
            self.tasks[task.task_id] = task
        self.optimize()

    def optimize(self):
        """Optimizes the timeline according to the chosen algorithm."""
        if self.algorithm == "FIFO":
            self.timeline = self.algorithm(
                list(self.tasks.items()), self.current_time, self.compute_physical_cost
            )
        else:
            raise ValueError("Invalid algorithm.")

    def update(self):
        """Updates the timeline."""
        self.update_time()
        self.update_physical_state()
        if new_task := self.next_task_in_timeline:
            if (
                self.current_task is None
                and self.current_time >= new_task.predicted_start_time
            ):
                self.current_task = self.timeline.get().task
                self.on_task_change(self.current_task)
            if (
                self.current_task
                and self.current_task.task_data.status == TaskStatus.DONE
            ):
                self.current_task = None
                self.on_task_change(None)

    @property
    def next_task_in_timeline(self) -> TaskInTimeline:
        """Gets next task in the timeline."""
        return None if self.timeline.empty() else self.timeline.queue[0]
