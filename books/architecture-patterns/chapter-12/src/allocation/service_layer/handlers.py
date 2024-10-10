import logging
from sqlalchemy import text

from src.allocation.adapters import email, redis_event_publisher
from src.allocation.domain.events import BatchCreated, AllocationRequired, OutOfStock, BatchQuantityChanged, Allocated, \
    Deallocated
from src.allocation.domain.model import Product, Batch, OrderLine
from src.allocation.service_layer.error import InvalidSku
from src.allocation.service_layer.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork
from src.allocation.service_layer.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


def add_batch(command: BatchCreated, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=command.sku)
        if product is None:
            product = Product(command.sku, batches=set([]))
            uow.products.add(product)

        product.batches.add(Batch(command.ref, command.sku, command.qty, command.eta))


def allocate(command: AllocationRequired, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(command.orderid, command.sku, command.qty)
    with uow:
        product = uow.products.get(sku=str(command.sku))
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batch_ref = product.allocate(line)
    return batch_ref


def send_out_of_stock_notification(event: OutOfStock):
    email.send_mail("stock@made.com", f"Out of stock for {event.sku}")


def change_batch_quantity(command: BatchQuantityChanged, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get_by_batchref(batchref=command.ref)
        product.change_batch_quantity(ref=command.ref, qty=command.qty)


def publish_allocated_event(event: Allocated, uow: AbstractUnitOfWork):
    logger.info("publish_allocated_event: %s", event)
    redis_event_publisher.publish('line_allocated', event)

def add_allocation_to_read_model(event: Allocated, uow:SqlAlchemyUnitOfWork):
    with uow:
        uow.session.execute(text("INSERT INTO allocations_view (orderid, sku, batchref) VALUES (:orderid, :sku, :batchref)"),dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref))

def remove_allocation_from_read_model(event: Deallocated, uow:SqlAlchemyUnitOfWork):
    with uow:
        uow.session.execute(text("DELETE FROM allocations_view WHERE orderid = :orderid AND sku = :sku"), dict(orderid=event.orderid, sku= event.sku))