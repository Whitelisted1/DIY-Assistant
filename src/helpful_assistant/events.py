from typing import Callable


class EventManager:
    """
    Not yet implemented
    """

    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name: str, callback: Callable) -> None:
        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(callback)

    def trigger_event(self, event_name: str, event_data: object) -> None:
        if event_name not in self.listeners:
            return

        for callback in self.listeners[event_name]:
            callback(event_data)
