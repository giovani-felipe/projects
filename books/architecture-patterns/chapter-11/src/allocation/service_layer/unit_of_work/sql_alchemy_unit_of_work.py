from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.allocation.adapters.repository import SqlAlchemyRepository, ProductSqlAlchemyRepository
from src.allocation.config import get_postgres_uri
from .abstract_unit_of_work import AbstractUnitOfWork

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(get_postgres_uri(), isolation_level='REPEATABLE READ'))


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.batches = SqlAlchemyRepository(self.session)
        self.products = ProductSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
