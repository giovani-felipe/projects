import time
from datetime import date
from typing import List

from src.allocation.domain import events
from src.allocation.domain.events import Event, BatchCreated, AllocationRequired, BatchQuantityChanged, OutOfStock
from src.allocation.service_layer.handlers import add_batch, allocate, send_out_of_stock_notification, \
    change_batch_quantity
from src.allocation.service_layer.message_bus.abstract_message_bus import AbstractMessageBus
from src.allocation.service_layer.message_bus.message_bus import MessageBus
from tests.unit.test_services import FakeUnitOfWork

now = time.time()


class FakeUnitOfWorkWithFakeMessageBus(FakeUnitOfWork):
    def __init__(self):
        super().__init__()
        self.events_published: List[Event] = []

    def publish_events(self):
        for product in self.products.seen:
            while product.events:
                self.events_published.append(product.events.pop(0))


class FakeMessageBus(AbstractMessageBus):
    def __init__(self):
        self.events_publish = []
        self.HANDLERS = {
            BatchCreated: [add_batch, lambda event, uow: self.events_publish.append(event)],
            AllocationRequired: [allocate, lambda event, uow: self.events_publish.append(event)],
            OutOfStock: [send_out_of_stock_notification, lambda event, uow: self.events_publish.append(event)],
            BatchQuantityChanged: [change_batch_quantity, lambda event, uow: self.events_publish.append(event)],
        }

    class TestAddBatch:
        def test_for_new_product(self):
            uow = FakeUnitOfWork()
            message_bus = MessageBus()
            message_bus.handle(events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow)
            assert uow.products.get("CRUNCHY-ARMCHAIR") is not None
            assert uow.commited

    class TestAllocate:
        def test_returns_allocation(self):
            uow = FakeUnitOfWork()
            message_bus = MessageBus()
            message_bus.handle(events.BatchCreated("batch1", "COMPLICATED-LAMP", 100, None), uow)
            [result] = message_bus.handle(events.AllocationRequired("o1", "COMPLICATED-LAMP", 10), uow)

            assert result == "batch1"

    class TestChangeBatchQuantity:
        def test_changes_available_quantity(self):
            uow = FakeUnitOfWork()
            message_bus = MessageBus()
            message_bus.handle(events.BatchCreated("batch1", "ADORABLE-SETTEE", 100, None), uow)
            [batch] = uow.products.get(sku="ADORABLE-SETTEE").batches
            assert batch.available_quantity == 100

            message_bus.handle(events.BatchQuantityChanged("batch1", 50), uow)
            assert batch.available_quantity == 50

        def test_reallocates_if_necessary(self):
            uow = FakeUnitOfWork()
            message_bus = MessageBus()
            event_history = [
                events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
                events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50, date.today()),
                events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
                events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20)
            ]

            for event in event_history:
                message_bus.handle(event, uow)

            [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
            assert batch1.available_quantity == 10
            assert batch2.available_quantity == 50

            message_bus.handle(events.BatchQuantityChanged("batch1", 25), uow)

            # order1 or order 1 will be deallocated, so we'll have 25 - 20
            assert batch1.available_quantity == 5
            # and 20 will be reallocated to the next batch
            assert batch2.available_quantity == 30

    def test_reallocates_if_necessary_isolated():
        uow = FakeUnitOfWorkWithFakeMessageBus()
        message_bus = FakeMessageBus()

        # test setup as before
        event_history = [
            BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
            BatchCreated("batch2", "INDIFFERENT-TABLE", 50, date.today()),
            AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
            AllocationRequired("order2", "INDIFFERENT-TABLE", 20)
        ]

        for event in event_history:
            message_bus.handle(event, uow)

        batches = uow.products.get(sku="INDIFFERENT-TABLE").batches

        [batch1, batch2] = list(batches)

        assert batch1.available_quantity == 10
        assert batch2.available_quantity == 50

        message_bus.handle(BatchQuantityChanged("batch1", 25), uow)

        # assert on new events emitted rather than downstream side-effects
        [reallocation_event] = uow.events_published
        assert isinstance(reallocation_event, AllocationRequired)
        assert reallocation_event.orderid in {'order1', 'order2'}
        assert reallocation_event.sku == 'INDIFFERENT-TABLE'
