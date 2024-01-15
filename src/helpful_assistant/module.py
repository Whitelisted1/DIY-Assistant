from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .action import Action


class Module:
    def __init__(self, name: str, definition: str, actions: List[Action] = []) -> None:
        self.name = name
        self.definition = definition
        self.actions = actions

    def add_action(self, action: Action):
        self.actions.append(action)
        action.category = self
