"""Contains types used by maweid."""
import typing as t
from collections import queue
from datetime import datetime

from .task import Task

TaskListType = t.List[Task]
"""Type for a list of tasks."""

PhysCostCallableType = t.Callable[[Task], float]
"""Type for a callable that computes the physical cost of a task."""

AlgorithmType = t.Callable[[datetime, TaskListType, PhysCostCallableType], queue.Queue]
"""Type for an algorithm function."""
