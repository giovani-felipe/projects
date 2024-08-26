from abc import ABC, abstractmethod
from typing import List

import pytest
from sqlalchemy.orm import Session

from src.allocation.domain.model import Batch, Product


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


class AbstractProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        raise NotImplementedError()

    @abstractmethod
    def get(self, sku: str) -> Product:
        raise NotImplementedError()


class ProductSqlAlchemyRepository(AbstractProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product):
        self.session.add(product)

    def get(self, sku: str) -> Product:
        return (self.session.query(Product)
                .filter_by(sku=sku)
                .with_for_update()
                .first())

    # def update(self, product: Product):
    #     self.session.execute(update(Product).where(sku=product.sku).values(product))
