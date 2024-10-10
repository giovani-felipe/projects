from abc import ABC, abstractmethod

from src.allocation.adapters.repository import AbstractRepository


class AbstractUnitOfWork(ABC):
    batches: AbstractRepository
    products: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        self._commit()
        self.collect_new_events()

    def collect_new_events(self):
        for product in self.products.seen:
            while product.events:
                yield product.events.pop(0)

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
