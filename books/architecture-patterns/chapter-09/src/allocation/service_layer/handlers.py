from src.allocation.adapters import email
from src.allocation.domain.events import BatchCreated, AllocationRequired, OutOfStock, BatchQuantityChanged
from src.allocation.domain.model import Product, Batch, OrderLine
from src.allocation.service_layer.error import InvalidSku
from src.allocation.service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork


def add_batch(event: BatchCreated, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=event.sku)
        if product is None:
            product = Product(event.sku, batches=set([]))
            uow.products.add(product)

        product.batches.add(Batch(event.ref, event.sku, event.qty, event.eta))


def allocate(event: AllocationRequired, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(event.orderid, event.sku, event.qty)
    with uow:
        product = uow.products.get(sku=str(event.sku))
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batch_ref = product.allocate(line)
    return batch_ref


def send_out_of_stock_notification(event: OutOfStock):
    email.send_mail("stock@made.com", f"Out of stock for {event.sku}")


def change_batch_quantity(event: BatchQuantityChanged, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get_by_batchref(batchref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
