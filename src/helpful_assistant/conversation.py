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
            history = [] if assistant is None else [Message("system", assistant.get_system_message())]

        if assistant is not None:
            assistant.event_manager.trigger_event("conversation_create", self)

        self.name = name
        self.history = history
        self.assistant = assistant
        self.discarded = False

    def get_by_role(self, role: str) -> List[Message]:
        """
        Fetches all messages by a specific role in the Conversation history.

        Parameters:
        role (str): the role to search for.

        Returns:
        List[Message]: A list of the messages by the specified role.
        """

        out = []
        for message in self.history:
            if message.role == role:
                out.append(message)
        return out

    def generate(self, prompt: str = None, *args, **kwargs) -> Union[Stream, str]:
        """
        Generates text from the Large Language Model.

        Parameters:
        prompt (str): The prompt for the model. Appends to conversation history.
        args (*args): Arguments to pass to the generate function.
        kwargs (**kwargs) Keyword arguments to pass to the generate function.

        Returns:
        Union[Stream, str]: Generated text or text Stream.
        """

        if self.assistant is None:
            raise RuntimeError("No assistant object specified in this conversation.")

        self._add_to_history(Message("user", prompt))

        return self.assistant.generate(conversation=self, *args, **kwargs)

    def discard(self) -> None:
        """
        Discards the conversation object. Main purpose is to trigger the "conversation_discarded" event.
        """

        if self.assistant is not None:
            self.assistant.remove_conversation(self)

        self.history.clear()
        self.assistant = None
        self.name = None
        self.discarded = True

    def _add_to_history(self, message: Message) -> None:
        """
        Adds a message to Conversation history.

        Parameters:
        message (Message): The Message object to add to conversation history.
        """

        self.history.append(message)
