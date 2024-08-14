from abc import ABC, abstractmethod
from typing import List

import pytest
from sqlalchemy.orm import Session

from domain.model import Batch


@pytest.mark.no_cover
class AbstractRepository(ABC):

    @abstractmethod
    def add(self, ref: str, sku: str, qty: int, eta=None):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, ref: str, sku: str, qty: int, eta=None):
        batch = Batch(ref, sku, qty, eta)
        self.session.add(batch)

    def get(self, reference) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()
