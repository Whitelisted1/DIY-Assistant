from __future__ import annotations
from typing import Callable, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .module import Module


class Action:
    def __init__(self, name: str, definition: str, task: Callable, category: Optional[Module] = None) -> None:
        self.name = name
        self.definition = definition
        self.task = task
        self.category = None

        if category is not None:
            category.add_action(self)
