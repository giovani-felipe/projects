from datetime import date, timedelta
from typing import Optional

import pytest

from src.allocation.adapters.repository import AbstractRepository
from src.allocation.domain.model import Batch, Product
from src.allocation.service_layer import services
from src.allocation.service_layer.unit_of_work import AbstractUnitOfWork

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


class FakeSession:
    commited = False

    def commit(self):
        self.commited = True


class FakeRepository(AbstractRepository):
    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product: Product):
        self._products.add(product)

    def _get(self, sku=None) -> Optional[Batch]:
        try:
            return next(product for product in self._products if product.sku == sku)
        except StopIteration:
            return None

    def list(self):
        return list(self._products)


class AbstractProductRepository:
    pass


class ProductFakeRepository(AbstractProductRepository):

    def __init__(self, products):
        self._products = set(products)
        self.seen = set()

    def add(self, product: Product):
        self._products.add(product)
        self.seen.add(product)

    def get(self, sku: str) -> Optional[Product]:
        try:
            return next(product for product in self._products if product.sku == sku)
        except StopIteration:
            return None


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.products = ProductFakeRepository([])

    def _commit(self):
        self.commited = True

    def rollback(self):
        pass


def test_returns_allocation():
    uow = FakeUnitOfWork()
    batch = Batch("batch1", "COMPLICATED-LAMP", 10, eta=None)
    product = Product("COMPLICATED-LAMP", [batch])
    uow.products.add(product)

    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)

    assert result == "batch1"


def test_error_for_invalid_sku():
    uow = FakeUnitOfWork()
    uow.products.add(Product("AREALSKU", [Batch("batch1", "AREALSKU", 100, eta=None)]))

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("order1", "NONEXISTENTSKU", 10, uow)


def test_commits():
    uow = FakeUnitOfWork()
    with uow:
        batch = Batch("batch1", "OMINOUS-MIRROR", 100, eta=None)
        product = Product("OMINOUS-MIRROR", [batch])
        uow.products.add(product)

    services.allocate("order1", "OMINOUS-MIRROR", 10, uow)
    assert uow.commited is True


def test_prefers_warehouse_batches_to_shipments():
    ref_in_stock_batch = "in-stock-batch"
    ref_shipment_batch = "shipment-batch"

    in_stock_batch = Batch(ref_in_stock_batch, "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch(ref_shipment_batch, "RETRO-CLOCK", 100, eta=tomorrow)

    uow = FakeUnitOfWork()
    uow.products.add(Product("RETRO-CLOCK", [in_stock_batch, shipment_batch]))

    services.allocate("oref", "RETRO-CLOCK", 10, uow)

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_add_batch_using():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "CRUNCHY-ARMCHAIR", 100, None, uow)

    [batch] = uow.products.get("CRUNCHY-ARMCHAIR").batches
    assert batch is not None
    assert uow.commited


def test_allocate_returns_allocation_using():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.allocate("order1", "COMPLICATED-LAMP", 10, uow)

    assert result == "batch1"


def test_allocate_errors_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "AREALSKU", 100, None, uow)

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("order1", "NONEXISTENTSKU", 10, uow)


def test_reallocate():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    services.allocate("order1", "COMPLICATED-LAMP", 10, uow)

    [batch] = uow.products.get(sku="COMPLICATED-LAMP").batches

    assert batch.reference == "batch1"
    assert batch.sku == "COMPLICATED-LAMP"
    assert batch.available_quantity == 90

    services.reallocate("order1", "COMPLICATED-LAMP", 10, uow)

    [batch] = uow.products.get(sku="COMPLICATED-LAMP").batches

    assert batch.reference == "batch1"
    assert batch.sku == "COMPLICATED-LAMP"
    assert batch.available_quantity == 90


def test_reallocate_errors():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    services.allocate("order1", "COMPLICATED-LAMP", 10, uow)

    [batch] = uow.products.get(sku="COMPLICATED-LAMP").batches

    assert batch.reference == "batch1"
    assert batch.sku == "COMPLICATED-LAMP"
    assert batch.available_quantity == 90

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.reallocate("order1", "NONEXISTENTSKU", 10, uow)


def test_change_batch_quantity():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "COMPLICATED-LAMP", 10, None, uow)
    services.allocate("order1", "COMPLICATED-LAMP", 10, uow)

    services.change_batch_quantity("COMPLICATED-LAMP", "batch1", 5, uow)

    [batch] = uow.products.get(sku="COMPLICATED-LAMP").batches

    assert batch.reference == "batch1"
    assert batch.sku == "COMPLICATED-LAMP"
    assert batch.available_quantity == 5
