import uuid

import pytest


def random_suffix():
    return uuid.uuid4().hex[:6]


def random(type: str, name: str = ""):
    return f"{type}-{name}-{random_suffix()}"


def random_sku(name=""):
    return random("sku", name)


def random_batchref(name=""):
    return random("batch", name)


def random_orderid(name=""):
    return random("order", name)


# @pytest.mark.usefixtures("restart_api")
@pytest.mark.e2e
def test_api_return_allocation(add_stock, client):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref("1")
    laterbatch = random_batchref("2")
    otherbatch = random_batchref("3")

    add_stock([
        (laterbatch, sku, 100, '2024-08-06'),
        (earlybatch, sku, 100, '2024-08-05'),
        (otherbatch, othersku, 100, None),
    ])

    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}

    # url = config.get_api_url()
    # response = requests.post(f"{url}/allocate", json=data)

    response = client.post("/allocate", json=data)

    assert response.status_code == 201
    assert response.json['batchref'] == earlybatch


# @pytest.mark.usefixtures("restart_api")
@pytest.mark.e2e
def test_allocations_are_persisted(add_stock, client):
    sku = random_sku()
    batch1, batch2 = random_batchref("1"), random_batchref("2")
    order1, order2 = random_orderid("1"), random_orderid("2")

    add_stock([(batch1, sku, 10, "2024-08-05"), (batch2, sku, 10, "2024-08-06")])
    line1 = {'orderid': order1, 'sku': sku, 'qty': 10}
    line2 = {'orderid': order2, 'sku': sku, 'qty': 10}
    # url = config.get_api_url()

    # first order uses up all stock in batch 1
    # response = requests.post(f"{url}/allocate", json=line1)
    response = client.post("/allocate", json=line1)

    assert response.status_code == 201
    assert response.json['batchref'] == batch1

    # second order should go to batch 2
    # response = requests.post(f"{url}/allocate", json=line2)
    response = client.post("/allocate", json=line2)

    assert response.status_code == 201
    assert response.json['batchref']


# @pytest.mark.usefixtures("restart_api")
@pytest.mark.e2e
def test_201_message_for_out_of_stock(add_stock, client):
    sku, small_batch, large_order = random_sku(), random_batchref(), random_orderid()
    add_stock([(small_batch, sku, 10, "2024-08-05")])

    data = {'orderid': large_order, 'sku': sku, 'qty': 20}

    # url = config.get_api_url()
    # response = requests.post(f"{url}/allocate", json=data)
    response = client.post("/allocate", json=data)

    # assert response.status_code == 400 when out of stock send a message about the request
    assert response.status_code == 201
    #assert response.json['message'] == f"Out of stock for sku {sku}"


# @pytest.mark.usefixtures("restart_api")
@pytest.mark.e2e
def test_400_message_for_invalid_sku(add_stock, client):
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {'orderid': orderid, 'sku': unknown_sku, 'qty': 20}

    # url = config.get_api_url()
    # response = requests.post(f"{url}/allocate", json=data)
    response = client.post("/allocate", json=data)

    assert response.status_code == 400
    assert response.json['message'] == f"Invalid sku {unknown_sku}"


# @pytest.mark.usefixtures("restart_api")
@pytest.mark.e2e
def test_happy_path_returns_201_and_allocated_batch_sku(add_stock, client):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref("1")
    laterbatch = random_batchref("2")
    otherbatch = random_batchref("3")

    add_stock([
        (laterbatch, sku, 100, '2024-08-06'),
        (earlybatch, sku, 100, '2024-08-05'),
        (otherbatch, othersku, 100, None),
    ])

    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}

    # url = config.get_api_url()
    # response = requests.post(f"{url}/allocate", json=data)
    response = client.post("/allocate", json=data)

    assert response.status_code == 201
    assert response.json['batchref'] == earlybatch


# @pytest.mark.usefixtures("restart_api")
@pytest.mark.e2e
def test_unhappy_path_returns_400_and_error_message(add_stock, client):
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {'orderid': orderid, 'sku': unknown_sku, 'qty': 20}

    # url = config.get_api_url()
    # response = requests.post(f"{url}/allocate", json=data)
    response = client.post("/allocate", json=data)

    assert response.status_code == 400
    assert response.json['message'] == f"Invalid sku {unknown_sku}"


def post_to_batches(ref, sku, qty, eta, client):
    response = client.post("/batches", json={'ref': ref, 'sku': sku, 'qty': qty, 'eta': eta})

    assert response.status_code == 201


@pytest.mark.e2e
def test_happy_path_returns_201_and_allocated_batch(client):
    sku, other_sku = random_sku(), random_sku("other")

    early_batch = random_batchref("1")
    later_batch = random_batchref("2")
    other_batch = random_batchref("3")

    post_to_batches(early_batch, sku, 100, '2024-08-13', client)
    post_to_batches(later_batch, sku, 100, '2024-08-14', client)
    post_to_batches(other_batch, other_sku, 100, None, client)

    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}

    response = client.post("/allocate", json=data)

    assert response.status_code == 201
    assert response.json['batchref'] == early_batch
