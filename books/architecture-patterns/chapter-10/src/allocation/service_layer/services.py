from datetime import date
from typing import Optional

from src.allocation.domain.model import OrderLine, Product, Batch, OrderReference, ProductReference, Quantity
from src.allocation.service_layer.error import InvalidSku
from src.allocation.service_layer.unit_of_work.sql_alchemy_unit_of_work import AbstractUnitOfWork


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(order_id: OrderReference, sku: ProductReference, qty: Quantity, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(order_id, sku, qty)
    with uow:
        product = uow.products.get(sku=str(sku))
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batch_ref = product.allocate(line)
    return batch_ref


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = Product(sku, batches=set([]))
            uow.products.add(product)

        product.batches.add(Batch(ref, sku, qty, eta))


def reallocate(orderid, sku, qty, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {sku}')
        batch = product.get_batch(sku=sku)
        batch.deallocate(OrderLine(orderid, sku, qty))
        allocate(orderid, sku, qty, uow)


def change_batch_quantity(sku: str, batchref: str, new_qty: int, uow: AbstractUnitOfWork):
    with uow:
        batch = uow.products.get(sku=sku).get_batch(reference=batchref)
        batch.change_purchased_quantity(new_qty)
        while batch.available_quantity < 0:
            batch.deallocate_one()
