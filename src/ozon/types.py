from dataclasses import (
    dataclass,
    field,
)


@dataclass
class OzonProduct:
    """DTO OZON товара."""

    name: str
    attributes: field(default_factory=list)
    category_id: int
    images: field(default_factory=list)
    offer_id: int
    old_price: str
    price: str
    vat: str
