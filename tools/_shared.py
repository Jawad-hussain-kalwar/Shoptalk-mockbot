import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_json(path_parts: List[str]) -> Any:
    path = os.path.join(ROOT, *path_parts)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_catalog() -> List[Dict[str, Any]]:
    return _read_json(["data", "catalog", "products.json"])  # type: ignore[no-any-return]


def load_inventory() -> List[Dict[str, Any]]:
    return _read_json(["data", "inventory", "inventory.json"])  # type: ignore[no-any-return]


def _price_to_float_cents(cents: int) -> float:
    return round(cents / 100.0, 2)


def _find_product_by_id(products: List[Dict[str, Any]], product_id: str) -> Optional[Dict[str, Any]]:
    for product in products:
        if product.get("id") == product_id:
            return product
    return None


def _find_variant_by_sku(product: Dict[str, Any], sku: str) -> Optional[Dict[str, Any]]:
    for variant in product.get("variants", []):
        if variant.get("sku") == sku:
            return variant
    return None


def _inventory_index_by_sku(inventory_rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {row["sku"]: row for row in inventory_rows}


@dataclass
class PriceBreakdown:
    subtotal_cents: int
    discount_cents: int
    tax_cents: int
    shipping_cents: int
    total_cents: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subtotalCents": self.subtotal_cents,
            "discountCents": self.discount_cents,
            "taxCents": self.tax_cents,
            "shippingCents": self.shipping_cents,
            "totalCents": self.total_cents,
            "subtotal": _price_to_float_cents(self.subtotal_cents),
            "discount": _price_to_float_cents(self.discount_cents),
            "tax": _price_to_float_cents(self.tax_cents),
            "shipping": _price_to_float_cents(self.shipping_cents),
            "total": _price_to_float_cents(self.total_cents),
        }



