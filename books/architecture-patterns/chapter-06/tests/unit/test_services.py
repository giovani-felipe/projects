from datetime import date, timedelta

import pytest

from src.allocation.adapters.repository import AbstractRepository
from src.allocation.domain.model import Batch
from src.allocation.service_layer import services

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


class FakeSession():
    commited = False

    def commit(self):
        self.commited = True


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._baches = set(batches)

    def add(self, ref, sku, qty, eta=None):
        self._baches.add(Batch(ref, sku, qty, eta))

    def get(self, reference) -> Batch:
        return next(batch for batch in self._baches if batch.reference == reference)

    def list(self):
        return list(self._baches)

    @staticmethod
    def for_batch(ref, sku, qty, eta=None):
        return FakeRepository([Batch(ref, sku, qty, eta)])


def test_returns_allocation():
    repo = FakeRepository.for_batch("batch1", "COMPLICATED-LAMP", 10, eta=None)

    result = services.allocate("o1", "COMPLICATED-LAMP", 10, repo, FakeSession())

    assert result == "batch1"


def test_error_for_invalid_sku():
    repo = FakeRepository.for_batch("batch1", "AREALSKU", 100, eta=None)

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("order1", "NONEXISTENTSKU", 10, repo, FakeSession())


def test_commits():
    repo = FakeRepository.for_batch("batch1", "OMINOUS-MIRROR", 100, eta=None)
    session = FakeSession()

    services.allocate("order1", "OMINOUS-MIRROR", 10, repo, session)
    assert session.commited is True


def test_prefers_warehouse_batches_to_shipments():
    ref_in_stock_batch = "in-stock-batch"
    ref_shipment_batch = "shipment-batch"
    repo = FakeRepository.for_batch(ref_in_stock_batch, "RETRO-CLOCK", 100, eta=None)
    repo.add(ref_shipment_batch, "RETRO-CLOCK", 100, eta=tomorrow)
    session = FakeSession()

    services.allocate("oref", "RETRO-CLOCK", 10, repo, session)

    in_stock_batch = repo.get(ref_in_stock_batch)
    shipment_batch = repo.get(ref_shipment_batch)

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_add_batch():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("batch1", "CRUNCHY-ARMCHAIR", 100, None, repo, session)

    assert repo.get("batch1") is not None
    assert session.commited


def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, repo, session)
    result = services.allocate("order1", "COMPLICATED-LAMP", 10, repo, session)

    assert result == "batch1"


def test_allocate_errors_for_invalid_sku():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("batch1", "AREALSKU", 100, None, repo, session)

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("order1", "NONEXISTENTSKU", 10, repo, session)
