import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from orm import mapper_registry, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine.connect()


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    session = sessionmaker()
    yield session(bind=in_memory_db)
    clear_mappers()
