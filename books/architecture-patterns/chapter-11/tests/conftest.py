import shutil
import subprocess
import time

import pytest
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, clear_mappers
from tenacity import retry, stop_after_delay

from src.allocation import config
from src.allocation.adapters.orm import mapper_registry, start_mappers
from src.allocation.entrypoints.flask_app import create_app


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine.connect()


@pytest.fixture
def session_factory(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(in_memory_db, monkeypatch):
    monkeypatch.setenv("TEST", "True")
    start_mappers()
    session = sessionmaker(bind=in_memory_db)
    yield session()
    clear_mappers()


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


@retry(stop=stop_after_delay(10))
def wait_for_redis_to_come_up():
    r = redis.Redis(**config.get_redis_host_and_port())
    return r.ping()


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    session = sessionmaker(bind=postgres_db)
    yield session()
    clear_mappers()


@pytest.fixture
def add_stock(postgres_session):
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            result = postgres_session.execute(text('SELECT id FROM products WHERE sku=:sku'), dict(sku=sku))

            if result.rowcount == 0:
                postgres_session.execute(
                    text('INSERT INTO products (sku, version_number) VALUES (:sku, :version_number)'),
                    dict(sku=sku, version_number=1))
                [[product_id]] = postgres_session.execute(text('SELECT id FROM products WHERE sku=:sku'), dict(sku=sku))
            else:
                [[product_id]] = result
            postgres_session.execute(
                text("INSERT INTO batches (reference, sku, purchased_quantity, eta, product_id)"
                     " VALUES (:ref, :sku, :qty, :eta, :product_id)"),
                dict(ref=ref, sku=sku, qty=qty, eta=eta, product_id=product_id),
            )
            [[batch_id]] = postgres_session.execute(text(
                "SELECT id FROM batches WHERE reference=:ref AND sku=:sku"),
                dict(ref=ref, sku=sku),
            )
            batches_added.add(batch_id)
            skus_added.add(sku)
        postgres_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        postgres_session.execute(
            text("DELETE FROM allocations WHERE batch_id=:batch_id"),
            dict(batch_id=batch_id),
        )
        postgres_session.execute(
            text("DELETE FROM batches WHERE id=:batch_id"), dict(batch_id=batch_id),
        )
    for sku in skus_added:
        postgres_session.execute(
            text("DELETE FROM order_lines WHERE sku=:sku"), dict(sku=sku),
        )
        postgres_session.commit()


# @pytest.fixture
# def restart_api():
#     (Path(__file__).parent.parent / "entrypoints" / "flask_app.py").touch()
#     time.sleep(0.5)
#     wait_for_webapp_to_come_up()


@pytest.fixture
def app(postgres_session):
    app = create_app({
        'TESTING': True
    })

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def restart_redis_pubsub():
    wait_for_redis_to_come_up()
    if not shutil.which("docker-compose"):
        print("skipping restart, assumes running in container")
        return

    subprocess.run(["docker-compose", "restart", "-t", "0", "redis_pubsub"], check=True)
