from typing import Dict, Type, Callable, List

from src.allocation.adapters import email
from src.allocation.domain.commands import Command, CreateBatch, Allocate, ChangeBatchQuantity
from src.allocation.domain.events import Event, OutOfStock, Allocated, Deallocated
from src.allocation.service_layer.handlers import add_batch, change_batch_quantity, allocate, publish_allocated_event, \
    add_allocation_to_read_model, remove_allocation_from_read_model
from src.allocation.service_layer.message_bus.abstract_message_bus import AbstractMessageBus
from src.allocation.service_layer.services import reallocate
from src.allocation.service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork


def send_out_of_stock_notification(event: OutOfStock, uow: AbstractUnitOfWork):
    email.send_mail('stock@made.com', f'Out of stock for {event.sku}')


class MessageBus(AbstractMessageBus):
    EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
        OutOfStock: [send_out_of_stock_notification],
        Allocated: [publish_allocated_event, add_allocation_to_read_model],
        Deallocated:[remove_allocation_from_read_model,reallocate]
    }

    COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
        CreateBatch: add_batch,
        ChangeBatchQuantity: change_batch_quantity,
        Allocate: allocate,
    }
