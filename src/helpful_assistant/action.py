from __future__ import annotations
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .module import Module


class Action:
    def __init__(self, name: str, definition: str, task: Callable, category: Module = None) -> None:
        self.name = name
        self.definition = definition
        self.task = task
        self.category = category
