from typing import Callable


class EventManager:
    """
    Not yet implemented
    """

    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name: str, callback: Callable) -> None:
        # make a dict entry if it is not already created
        if event_name not in self.listeners:
            self.listeners[event_name] = []

        # append listener to dict entry
        self.listeners[event_name].append(callback)

    def trigger_event(self, event_name: str, event_data: object) -> None:
        # if the event does not have any listeners then stop
        if event_name not in self.listeners:
            return

        # call the listeners
        for callback in self.listeners[event_name]:
            callback(event_data)
