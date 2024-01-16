from __future__ import annotations
from typing import List, TYPE_CHECKING, Union, Generator

if TYPE_CHECKING:
    from .assistant import Assistant


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content


class Conversation:
    def __init__(self, name: str = "Conversation", history: List[Message] = [], assistant: Union[Assistant, None] = None):
        self.name = name
        self.history = history
        self.assistant = assistant

    def add_to_history(self, message: Message):
        self.history.append(message)

    def generate(self, *args, **kwargs) -> Union[Generator, str]:
        if self.assistant is None:
            raise RuntimeError("No assistant object specified in this conversation.")

        return self.assistant.generate(conversation=self, *args, **kwargs)
