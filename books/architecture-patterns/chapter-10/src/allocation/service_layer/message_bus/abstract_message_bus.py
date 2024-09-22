from typing import Dict, Type, Callable, List, Union
from venv import logger

from tenacity import Retrying, stop_after_attempt, wait_exponential, RetryError

from src.allocation.domain.command import Command
from src.allocation.domain.events import Event
from src.allocation.service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork

Message = Union[Command, Event]


class AbstractMessageBus:
    EVENT_HANDLERS: Dict[Type[Event], List[Callable]]
    COMMANDS_HANDLERS: Dict[Type[Event], List[Callable]]

    def handle(self, message: Message, uow: AbstractUnitOfWork):
        results = []
        queue = [message]
        while queue:
            message = queue.pop(0)
            for handler in self.HANDLERS[type(message)]:
                results.append(handler(message, uow=uow))
                queue.extend(uow.collect_new_events())
        return results

    def handle_event(self, event: Event, queue: List[Message], uow: AbstractUnitOfWork):
        for handler in self.EVENT_HANDLERS[type(event)]:
            try:
                for attempt in Retrying(stop=stop_after_attempt(3), wait=wait_exponential()):
                    with attempt:
                        logger.debug('handlig event %s  with handler %s', event, handler)
                        handler(event, uow=uow)
                        queue.extend(uow.collect_new_events())
            except RetryError as err:
                logger.error('Failed to handle event %s times, giving up!', err.last_attempt.attempt_number)
                continue

    def handle_command(self, command: Command, queue: List[Message], uow: AbstractUnitOfWork):
        logger.debug('handling command %s', command)
        try:
            handler = self.COMMANDS_HANDLERS[type(command)]
            result = handler(command, uow=uow)
            queue.extend(uow.collect_new_events())
            return result
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise
