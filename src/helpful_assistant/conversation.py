from __future__ import annotations
from typing import List, TYPE_CHECKING, Union, Generator, Optional
from .stream import Stream

if TYPE_CHECKING:
    from .assistant import Assistant


class Message:
    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __str__(self) -> str:
        return self.content


class Conversation:
    def __init__(self, name: str = "Conversation", history: Optional[List[Message]] = None, assistant: Optional[Assistant] = None) -> None:
        if history is None:
            history = []
            if assistant is not None:
                assistant.event_manager.trigger_event("conversation_create", self)
                history = [Message("system", assistant.get_system_message())]

        self.name = name
        self.history = history
        self.assistant = assistant
        self.discarded = False

    def get_by_role(self, role: str) -> List[Message]:
        out = []
        for message in self.history:
            if message.role == role:
                out.append(message)
        return out

    def _add_to_history(self, message: Message) -> None:
        self.history.append(message)

    def generate(self, prompt: str = None, *args, **kwargs) -> Union[Stream, str]:
        if self.assistant is None:
            raise RuntimeError("No assistant object specified in this conversation.")

        self._add_to_history(Message("user", prompt))

        return self.assistant.generate(conversation=self, *args, **kwargs)

    def discard(self):
        if self.assistant is not None:
            self.assistant.event_manager.trigger_event("conversation_discard", self)

        self.history.clear()
        self.assistant = None
        self.name = None
        self.discarded = True
