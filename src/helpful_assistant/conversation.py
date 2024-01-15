from typing import List


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content


class Conversation:
    def __init__(self, name: str = "Conversation", history: List[Message] = []):
        self.name = name
        self.history = history

    def add_to_history(self, message: Message):
        self.history.append(message)
