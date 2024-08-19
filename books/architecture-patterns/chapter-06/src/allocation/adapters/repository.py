from abc import ABC, abstractmethod
from typing import List

import pytest
from sqlalchemy.orm import Session

from src.allocation.domain.model import Batch


@pytest.mark.no_cover
class AbstractRepository(ABC):

    @abstractmethod
    def add(self, ref: str, sku: str, qty: int, eta=None):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference=None, sku=None) -> Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, ref: str, sku: str, qty: int, eta=None):
        batch = Batch(ref, sku, qty, eta)
        self.session.add(batch)

    def get(self, reference=None, sku=None) -> Batch:
        if reference is not None:
            return self.session.query(Batch).filter_by(reference=reference).one()
        elif sku is not None:
            return self.session.query(Batch).filter_by(sku=sku).one()

        return None

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()
