from sqlalchemy import Column, Integer, String, Table, Date, ForeignKey, event
from sqlalchemy.orm import registry, relationship

from src.allocation.domain.model import OrderLine, Batch, Product

mapper_registry = registry()

order_line = Table(
    "order_lines", mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches", mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
    Column("product_id", ForeignKey("products.id"))
)

allocations = Table(
    "allocations", mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id"))
)

products = Table("products", mapper_registry.metadata,
                 Column("id", Integer, primary_key=True, autoincrement=True),
                 Column("sku", String(255)),
                 Column("version_number", Integer))


def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(OrderLine, order_line)
    batches_mapper = mapper_registry.map_imperatively(Batch, batches, properties={
        "_allocations": relationship(lines_mapper, secondary=allocations, collection_class=set),
        "_purchased_quantity": batches.c.purchased_quantity
    })
    mapper_registry.map_imperatively(Product, products, properties={
        "batches": relationship(batches_mapper, collection_class=set)
    })


@event.listens_for(Product, "load")
def receive_load(product, _):
    product.events = []
