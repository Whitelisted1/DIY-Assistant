from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .action import Action


class Module:
    def __init__(self, name: str, definition: str, actions: Optional[List[Action]] = None) -> None:
        if actions is None:
            actions = []

        self.name = name
        self.definition = definition
        self.actions = actions

    def add_action(self, action: Action) -> None:
        self.actions.append(action)
        action.category = self

    def convert_actions_to_llm_readable(self) -> str:
        return "\n".join([f"{action.name} ({action.definition})" for action in self.actions])
