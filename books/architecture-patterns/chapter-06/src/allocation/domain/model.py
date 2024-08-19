from dataclasses import dataclass
from datetime import date
from typing import Optional, Set, NewType, List

OrderReference = NewType("OrderReference", int)
Quantity = NewType("Quantity", int)
ProductReference = NewType("ProductReference", int)
Reference = NewType("Reference", int)


# OrderLine is a value object
@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: OrderReference
    sku: ProductReference
    qty: Quantity


class Batch:

    def __init__(self, ref: Reference, sku: ProductReference, qty: Quantity, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def deallocate(self, line):
        if line in self._allocations:
            self._allocations.remove(line)

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def change_purchased_quantity(self, new_qty: int):
        self._purchased_quantity = new_qty

    def deallocate_one(self):
        self._allocations.pop()


def allocate(line: OrderLine, batches: List[Batch]):
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")


def deallocate(line: OrderLine, batches: List[Batch]):
    batch = next(b for b in sorted(batches))
    batch.deallocate(line)
    return batch.reference


class OutOfStock(Exception):
    pass


class SkuNotFound(Exception):
    pass
