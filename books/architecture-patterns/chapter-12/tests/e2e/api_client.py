from flask.testing import FlaskClient

from tests.conftest import client


def post_to_add_batch(ref, sku, qty, eta, client: FlaskClient):
    response = client.post("/batches", json={"ref": ref, "sku": sku, "qty": qty, "eta": eta})
    assert response.status_code == 201


def post_to_allocate(orderid, sku, qty, client: FlaskClient, expect_success=True):
    response = client.post("/allocate", json={"orderid": orderid, "sku": sku, "qty": qty})

    if expect_success:
        assert response.status_code == 201
    return response


def get_allocation(orderid, client: FlaskClient):
    return client.get(f"/allocations/{orderid}")
