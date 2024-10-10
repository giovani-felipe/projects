from src.allocation.adapters.redis_event_publisher import get_readmodel
from src.allocation.domain.model import Batch, OrderLine
from src.allocation.service_layer.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork


def allocations(orderid: str, uow: SqlAlchemyUnitOfWork):
    with uow:
        batches = uow.session.query(Batch).join(
            OrderLine, Batch._allocations
        ).filter(
            OrderLine.orderid == orderid
        )
        return [{"sku": batch.sku, "batchref": batch.reference} for batch in batches]

# def allocations(orderid: str):
#     batches = get_readmodel(orderid)
#     return [{'batchref':batch.decode(), 'sku':sku.decode()} for sku, batch in batches.items()]
