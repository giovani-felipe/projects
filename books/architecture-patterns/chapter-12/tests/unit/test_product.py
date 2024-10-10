from datetime import date

from src.allocation.domain import events
from src.allocation.domain.model import Batch, Product, OrderLine

today = date.today()


def test_records_out_of_stock_event_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    product = Product(sku='SMALL-FORK', batches=[batch])
    product.allocate(OrderLine('order1', 'SMALL-FORK', 10))

    allocation = product.allocate(OrderLine('order2', 'SMALL-FORK', 1))
    assert product.events[-1] == events.OutOfStock(sku='Out of stock for sku SMALL-FORK')
    assert allocation is None
