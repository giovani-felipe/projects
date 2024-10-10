from src.allocation import views
from src.allocation.domain import commands, events
from src.allocation.service_layer.message_bus.message_bus import MessageBus
from src.allocation.service_layer.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork
from tests.util import today


def test_allocations_view(sqlite_session_factory):
    uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
    message_bus = MessageBus()
    message_bus.handle(commands.CreateBatch("sku1batch","sku1", 50, None), uow)
    message_bus.handle(commands.CreateBatch("sku2batch","sku2", 50, today), uow)
    message_bus.handle(commands.Allocate("order1","sku1", 20), uow)
    message_bus.handle(commands.Allocate("order1", "sku2", 20), uow)
    # add a spurious batch and order to make sure we´re getting the right ones
    message_bus.handle(commands.CreateBatch("sku1batch-later","sku1", 50, today), uow)
    message_bus.handle(commands.Allocate("otherorder","sku1", 30), uow)
    message_bus.handle(commands.Allocate("otherorder","sku1",10), uow)

    assert views.allocations("order1", uow) == [
        {"sku":"sku1","batchref": "sku1batch"},
        {"sku": "sku2", "batchref": "sku2batch"}
    ]


def test_deallocation(sqlite_session_factory):
    uow = SqlAlchemyUnitOfWork(sqlite_session_factory)
    message_bus = MessageBus()
    message_bus.handle(commands.CreateBatch("b1", "sku1", 50, None), uow)
    message_bus.handle(commands.CreateBatch("b2", "sku1", 50, today), uow)
    message_bus.handle(commands.Allocate("o1", "sku1", 40), uow)
    message_bus.handle(commands.ChangeBatchQuantity("b1", 10), uow)

    assert views.allocations("o1", uow) == [
        {"sku": "sku1", "batchref": "b2"},
    ]