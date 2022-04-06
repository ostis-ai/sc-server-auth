"""
    Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikiforov Sergei
    Author Alexandr Zagorskiy
"""

from abc import ABC, abstractmethod

from json_client import client
from json_client.dataclass import ScAddr, ScEvent
from json_client.sc_keynodes import ScKeynodes


class ScAgent(ABC):
    keynodes = ScKeynodes()

    def __init__(self):
        self._event = self.register()

    def _get_event(self):
        return self._event

    def _set_event(self, event: ScEvent):
        if not isinstance(event, ScEvent):
            raise TypeError("Event must be an instance of ScEvent")
        self._event = event

    event = property(_get_event, _set_event)

    @abstractmethod
    def register(self) -> ScEvent:
        pass

    def unregister(self) -> None:
        client.events_destroy([self.event])

    @staticmethod
    @abstractmethod
    def run_impl(action_class: ScAddr, edge: ScAddr, action_node: ScAddr) -> None:
        pass
