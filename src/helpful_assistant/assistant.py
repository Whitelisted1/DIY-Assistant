from typing import Union, List, Generator
from .conversation import Conversation, Message


class Assistant:
    def __init__(self, llm_class: object, *args, **kwargs) -> None:
        self.llm = llm_class
        self.conversation_list = []

    def new_conversation(self, name: str = "Conversation", history: List[Message] = []) -> Conversation:
        c = Conversation(name=name, history=history, assistant=self)
        self.conversation_list.append(c)
        return c

    def generate(self, user_input: str, stream: bool = False, allow_action_execution: bool = True) -> Union[Generator, str]:
        pass
