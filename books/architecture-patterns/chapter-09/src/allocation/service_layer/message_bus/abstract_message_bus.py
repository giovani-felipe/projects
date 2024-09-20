from typing import Dict, Type, Callable, List

from src.allocation.domain.events import Event
from src.allocation.service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork


class AbstractMessageBus:
    HANDLERS: Dict[Type[Event], List[Callable]]

    def handle(self, event: Event, uow: AbstractUnitOfWork):
        results = []
        queue = [event]
        while queue:
            event = queue.pop(0)
            for handler in self.HANDLERS[type(event)]:
                results.append(handler(event, uow=uow))
                queue.extend(uow.collect_new_events())
        return results
