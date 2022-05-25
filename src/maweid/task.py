"""Functions relating to tasks and data structures for them."""
import typing as t
import uuid
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from enum import Enum

T = t.TypeVar("T")


class InvalidTaskError(Exception):
    """Exception raised when a task is invalid."""

    pass


class TaskPriority(Enum):
    """Describes the priority of a task."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    IMMEDIATE = 5


class TaskStatus(Enum):
    """Describes the status of a task."""

    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    CANCELLED = 4
    ERROR = 5


@dataclass
class TaskData(t.Generic[T]):
    """General data contained for all tasks."""

    information: T
    """User defined information about the task. Can be anything."""

    submission_time: datetime
    """Submission time of the task."""
    priority: TaskPriority
    """Priority of the task."""
    deadline: datetime
    """Deadline for execution of the task."""
    duration: timedelta
    """Duration of the task."""
    status: TaskStatus = TaskStatus.TODO
    """Status of the task."""
    description: str = ""
    """Description of the task."""
    started: datetime = None


# TODO: Add more constraints
class TaskConstraints:
    """Individual constraints for a task."""

    time_constraints: t.List[datetime] = None
    """Time constraints for a task."""


class Task(ABC, t.Generic[T]):
    """Abstract class for tasks.

    Implementing this should require

    """

    def __init__(self, task_data: TaskData[T]):
        """Initialize a task."""
        self.task_data = task_data
        self.unique_id = uuid.uuid4()
        self._validate_task()
        self.compute_constraints()

    def _validate_task(self):
        """Validates the task.

        Should raise error if task is not valid. For example
        if the task submission time is in the future or
        the deadline is in the past.
        """
        if self.task_data.deadline < self.task_data.submission_time:
            raise InvalidTaskError("Task deadline is in the past.")
        self.validate()

    @property
    def task_id(self):
        """Returns the unique task id."""
        return self.unique_id.hex

    def validate(self):
        """Custom validation of task.

        Should raise :class:`~InvalidTaskException` if task is not valid.
        """
        pass

    def constraints(self):
        """Run once on initialization to compute constraints.

        Should raise error if constraints are not valid. For example
        if a time constraint is not valid within the deadlines.

        """
        self.compute_constraints = TaskConstraints()
