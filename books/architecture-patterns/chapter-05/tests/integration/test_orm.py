from sqlalchemy import text
from sqlalchemy.orm import Session

from domain.model import OrderLine


def test_orderline_mapper_can_load_lines(session: Session):
    session.execute(text('INSERT INTO order_lines (orderid, sku, qty) VALUES '
                         '("order1", "RED-CHAIR", 12),'
                         '("order2", "RED-TABLE", 13),'
                         '("order3", "BLUE-LIPSTICK", 14)'))

    expected = [
        OrderLine("order1", "RED-CHAIR", 12),
        OrderLine("order2", "RED-TABLE", 13),
        OrderLine("order3", "BLUE-LIPSTICK", 14)
    ]

    assert session.query(OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session: Session):
    new_line = OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT orderid, sku, qty from "order_lines"')))

    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
