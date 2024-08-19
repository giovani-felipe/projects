from datetime import date
from typing import Optional

from src.allocation.domain import model
from src.allocation.domain.model import OrderLine
from src.allocation.service_layer.unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(sku, batches):
            raise InvalidSku(f"Invalid sku {sku}")
        line = OrderLine(orderid, sku, qty)
        batchref = model.allocate(line, batches)
        return batchref


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], uow: AbstractUnitOfWork):
    with uow:
        uow.batches.add(ref, sku, qty, eta)


def reallocate(orderid, sku, qty, uow: AbstractUnitOfWork):
    with uow:
        batch = uow.batches.get(sku=sku)
        if batch is None:
            raise InvalidSku(f'Invalid sku {sku}')
        batch.deallocate(OrderLine(orderid, sku, qty))
        allocate(orderid, sku, qty, uow)


def change_batch_quantity(batchref: str, new_qty: int, uow: AbstractUnitOfWork):
    with uow:
        batch = uow.batches.get(reference=batchref)
        batch.change_purchased_quantity(new_qty)
        while batch.available_quantity < 0:
            batch.deallocate_one()
