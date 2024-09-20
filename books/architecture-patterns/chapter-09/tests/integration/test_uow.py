import threading
import time
import traceback
from typing import List

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.allocation.domain.model import OrderLine
from src.allocation.service_layer import unit_of_work
from src.allocation.service_layer.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork
from tests.e2e.test_api import random_sku, random_batchref, random_orderid


def insert_batch(session: Session, ref, sku, qty, eta, product_version=0):
    session.execute(text('INSERT INTO products (sku, version_number) VALUES (:sku, :version_number)'),
                    dict(sku=sku, version_number=product_version))

    [[product_id]] = session.execute(text('SELECT id FROM products WHERE sku=:sku'), dict(sku=sku))

    session.execute(text('INSERT INTO batches (reference, sku, purchased_quantity, eta, product_id) '
                         'VALUES (:ref, :sku, :qty, :eta, :product_id)'),
                    dict(ref=ref, sku=sku, qty=qty, eta=eta, product_id=product_id))


def get_allocated_batch_ref(session: Session, orderid, sku):
    [[orderlineid]] = session.execute(text('SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku'),
                                      dict(orderid=orderid, sku=sku))
    [[batchref]] = session.execute(text('SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id '
                                        'WHERE orderline_id=:orderlineid'), dict(orderlineid=orderlineid))
    return batchref


def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session = session_factory()
    insert_batch(session, 'batch1', 'HIPSTER-WORKBENCH', 100, None)

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        batch = uow.batches.get(sku='HIPSTER-WORKBENCH')
        line = OrderLine('order1', 'HIPSTER-WORKBENCH', 10)
        batch.allocate(line)

    batchref = get_allocated_batch_ref(session, 'order1', 'HIPSTER-WORKBENCH')
    assert batchref == 'batch1'


# def test_rolls_back_uncommitted_work_by_default(session_factory):
#     uow = SqlAlchemyUnitOfWork(session_factory)
#     with uow:
#         insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)
#
#     new_session = session_factory()
#     rows = list(new_session.execute(text('SELECT * FROM "batches"')))
#     assert rows == []


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute(text('SELECT * FROM "batches"')))
    assert rows == []


def test_get_batches_without_params(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        batch = uow.batches.get()

    assert batch is None


def try_to_allocate(orderid, sku, exceptions):
    line = OrderLine(orderid, sku, 10)
    try:
        with unit_of_work.SqlAlchemyUnitOfWork() as uow:
            product = uow.products.get(sku=sku)
            product.allocate(line)
            time.sleep(0.2)
    except Exception as err:
        print(traceback.format_exc())
        exceptions.append(err)


@pytest.mark.skip()
def test_concurrent_updates_to_version_are_not_allowed(postgres_session):
    sku, batch = random_sku(), random_batchref()
    session = postgres_session
    insert_batch(session, batch, sku, 100, eta=None, product_version=1)
    session.commit()

    order1, order2 = random_orderid(1), random_orderid(2)
    exceptions: List[Exception] = []
    try_to_allocate_order1 = lambda: try_to_allocate(order1, sku, exceptions)
    try_to_allocate_order2 = lambda: try_to_allocate(order2, sku, exceptions)
    thread1 = threading.Thread(target=try_to_allocate_order1)
    thread2 = threading.Thread(target=try_to_allocate_order2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    [[version]] = session.execute(text("SELECT version_number FROM products WHERE sku=:sku"), dict(sku=sku))

    assert version == 2
    [exception] = exceptions
    assert 'could not serialize access due to concurrent update' in str(exception)

    orders = list(session.execute(text(
        "SELECT orderid FROM allocations "
        "JOIN batches ON allocations.batch_id = batches.id "
        "JOIN order_lines ON allocations.orderline_id = order_lines.id "
        "WHERE order_lines.sku=:sku"), dict(sku=sku)
    ))

    assert len(orders) == 1
    with unit_of_work.SqlAlchemyUnitOfWork() as uow:
        uow.session.execute(text("SELECT 1"))
