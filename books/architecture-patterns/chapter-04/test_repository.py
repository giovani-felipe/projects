from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from model import Batch, OrderLine
from repository import SqlAlchemyRepository, AbstractRepository


class FakeRepository(AbstractRepository):

    def __init__(self, batches: List[Batch]):
        self._batches = set(batches)

    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, reference) -> Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


def test_repository_can_save_a_batch(session: Session):
    batch = Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = list(session.execute(text('SELECT reference, sku, _purchased_quantity, eta FROM "batches"')))

    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def insert_order_line(session: Session):
    session.execute(text('INSERT INTO order_lines (orderid, sku, qty) VALUES ("order1", "GENERIC-SOFA", 12)'))
    [[orderline_id]] = session.execute(
        text('SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku'),
        dict(orderid="order1", sku="GENERIC-SOFA"))
    return orderline_id


def insert_batch(session: Session, batch_id: str):
    session.execute(text('INSERT INTO batches (reference, sku, _purchased_quantity, eta) '
                         'VALUES (:batch_id, "GENERIC-SOFA", 100, null)'), dict(batch_id=batch_id))
    [[batch_id]] = session.execute(text('SELECT id FROM batches WHERE  reference=:batch_id AND sku="GENERIC-SOFA"'),
                                   dict(batch_id=batch_id))
    return batch_id


def insert_allocation(session: Session, orderline_id: int, batch_id):
    session.execute(text('INSERT INTO allocations (orderline_id, batch_id) '
                         'VALUES (:orderline_id, :batch_id)'), dict(orderline_id=orderline_id, batch_id=batch_id))


def test_repository_can_retrive_a_batch_with_allocations(session: Session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {OrderLine("order1", "GENERIC-SOFA", 12)}
