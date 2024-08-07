import pytest

import model
import services
from model import Batch
from repository import AbstractRepository


class FakeSession():
    commited = False

    def commit(self):
        self.commited = True


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._baches = set(batches)

    def add(self, batch):
        self._baches.add(batch)

    def get(self, reference) -> Batch:
        return next(batch for batch in self._baches if batch.reference == reference)

    def list(self):
        return list(self._baches)


def test_returns_allocation():
    line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED-LAMP", 10, eta=None)

    repo = FakeRepository([batch])

    result = services.allocate(line, repo, FakeSession())

    assert result == "b1"


def test_error_for_invalid_sku():
    line = model.OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = model.Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate(line, repo, FakeSession())


def test_commits():
    line = model.OrderLine("o1", "OMINOUS-MIRROR", 10)
    batch = model.Batch("b1", "OMINOUS-MIRROR", 100, eta=None)

    repo = FakeRepository([batch])
    session = FakeSession()

    services.allocate(line, repo, session)
    assert session.commited is True
