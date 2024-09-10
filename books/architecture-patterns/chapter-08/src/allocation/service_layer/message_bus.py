from typing import Dict, Callable, List, Type

from src.allocation.adapters import email
from src.allocation.domain.events import Event, OutOfStock


def handle(event: Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_out_of_stock_notification(event: OutOfStock):
    email.send_mail('stock@made.com', f'Out of stock for {event.sku}')


HANDLERS: Dict[Type[Event], List[Callable]] = {
    OutOfStock: [send_out_of_stock_notification]
}
