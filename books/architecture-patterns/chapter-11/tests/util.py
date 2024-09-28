import uuid


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
