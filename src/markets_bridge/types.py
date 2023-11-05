from dataclasses import (
    dataclass,
    field,
)
from decimal import (
    Decimal,
)


@dataclass
class MBProduct:
    external_id: int
    translated_name: str
    price: Decimal
    discounted_price: Decimal
    category_external_id: int
    characteristic_values: field(default_factory=list)
    images: field(default_factory=list)

