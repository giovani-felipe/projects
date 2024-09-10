from abc import ABC, abstractmethod
from typing import Set, Optional, Type

import pytest
from sqlalchemy.orm import Session

from src.allocation.domain.model import Product


@pytest.mark.no_cover
class AbstractRepository(ABC):

    def __init__(self):
        self.seen: Set[Product] = set()

    def add(self, product: Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku=None) -> Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abstractmethod
    def _add(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def _get(self, sku: str = None) -> Optional[Product]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, product: Product):
        self.session.add(product)

    def _get(self, sku: str = None) -> Optional[Product]:
        return self.session.query(Product).filter_by(sku=sku).first()

    def list(self) -> list[Type[Product]]:
        return self.session.query(Product).all()


class ProductSqlAlchemyRepository(SqlAlchemyRepository):
    def __init__(self, session: Session):
        super().__init__(session)
        self.session = session

    def _add(self, product: Product):
        self.session.add(product)

    def _get(self, sku: str = None) -> Optional[Product]:
        return (self.session.query(Product)
                .filter_by(sku=sku)
                .with_for_update()
                .first())


class TrackingRepository:
    seen: Set[Product]

    def __init__(self, repo: AbstractRepository):
        self.seen = set()
        self._repo = repo

    def add(self, product: Product):
        self._repo.add(product)
        self.seen.add(product)

    def get(self, sku: str) -> Product:
        product = self._repo.get(sku)
        if product:
            self.seen.add(product)
        return product
