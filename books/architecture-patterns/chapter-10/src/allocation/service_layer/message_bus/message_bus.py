from typing import Dict, Type, Callable, List

from src.allocation.adapters import email
from src.allocation.domain.command import Command
from src.allocation.domain.events import Event, BatchCreated, BatchQuantityChanged, AllocationRequired, OutOfStock
from src.allocation.service_layer.handlers import add_batch, change_batch_quantity, allocate
from src.allocation.service_layer.message_bus.abstract_message_bus import AbstractMessageBus
from src.allocation.service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork


def send_out_of_stock_notification(event: OutOfStock, uow: AbstractUnitOfWork):
    email.send_mail('stock@made.com', f'Out of stock for {event.sku}')


class MessageBus(AbstractMessageBus):
    EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
        OutOfStock: [send_out_of_stock_notification]
    }

    COMMAND_HANDLERS: Dict[Type[Command], List[Callable]] = {
        BatchCreated: [add_batch],
        BatchQuantityChanged: [change_batch_quantity],
        AllocationRequired: [allocate],
    }
