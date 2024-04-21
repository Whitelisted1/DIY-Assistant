from typing import Callable


class EventManager:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name: str, callback: Callable[[object], None]) -> None:
        """
        Add a listener to a given event.

        Parameters:
        event_name (str): The event name. Ex: "conversation_create".
        callback (Callable[[object], None]): Callback for when the event is triggered. Callback should take one argument, and return None.
        """

        # make a dict entry if it is not already created
        if event_name not in self.listeners:
            self.listeners[event_name] = []

        # append listener to dict entry
        self.listeners[event_name].append(callback)

    def trigger_event(self, event_name: str, event_data: object) -> None:
        """
        Trigger an event given an event name and data for the listeners.

        Parameters:
        event_name (str): Name of the event.
        event_data (object): The event data which will be passed to the listeners.
        """
        # if the event does not have any listeners then stop
        if event_name not in self.listeners:
            return

        # call the listeners
        for callback in self.listeners[event_name]:
            callback(event_data)
