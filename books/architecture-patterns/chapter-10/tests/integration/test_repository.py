import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.allocation.adapters.repository import SqlAlchemyRepository, TrackingRepository, ProductSqlAlchemyRepository
from src.allocation.domain.model import Batch, Product


@pytest.mark.skip()
def test_repository_can_save_a_batch(session: Session):
    repo = SqlAlchemyRepository(session)
    repo.add("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    session.commit()

    rows = repo.list()
    expected = rows[0]

    assert expected.reference == "batch1"
    assert expected.sku == "RUSTY-SOAPDISH"
    assert expected.available_quantity == 100
    assert expected.eta == None


def insert_order_line(session: Session):
    session.execute(text('INSERT INTO order_lines (orderid, sku, qty) VALUES ("order1", "GENERIC-SOFA", 12)'))
    [[orderline_id]] = session.execute(
        text('SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku'),
        dict(orderid="order1", sku="GENERIC-SOFA"))
    return orderline_id


def insert_batch(session: Session, batch_id: str):
    session.execute(text('INSERT INTO products (sku, version_number) VALUES (:sku, :version_number)'),
                    dict(sku='GENERIC-SOFA', version_number=0))

    [product_id] = session.execute(text('SELECT id FROM products WHERE sku=:sku'), dict(sku='GENERIC-SOFA')).first()

    session.execute(text('INSERT INTO batches (reference, sku, purchased_quantity, eta, product_id) '
                         'VALUES (:batch_id, "GENERIC-SOFA", 100, null, :product_id)'),
                    dict(batch_id=batch_id, product_id=product_id))
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

    repo = TrackingRepository(ProductSqlAlchemyRepository(session))
    retrieved = repo.get(sku="GENERIC-SOFA")

    expected = Product(sku="GENERIC-SOFA", batches=set([Batch("batch1", "GENERIC-SOFA", 100, eta=None)]))

    assert retrieved.sku == expected.sku
    assert retrieved.batches.copy().pop()._purchased_quantity == expected.batches.copy().pop()._purchased_quantity
