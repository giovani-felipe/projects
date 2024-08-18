from datetime import date
from typing import Optional

from src.allocation.adapters.repository import AbstractRepository
from src.allocation.domain import model
from src.allocation.domain.model import OrderLine


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(orderid: str, sku: str, qty: int, repository: AbstractRepository, session) -> str:
    batches = repository.list()
    if not is_valid_sku(sku, batches):
        raise InvalidSku(f"Invalid sku {sku}")
    line = OrderLine(orderid, sku, qty)
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], repo: AbstractRepository, session):
    repo.add(ref, sku, qty, eta)
    session.commit()
