import json
import logging
import os
import inspect
from functools import wraps
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _format_for_log(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, indent=2, default=str)
    except Exception:
        try:
            return str(value)
        except Exception:
            return repr(value)


def log_tool_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        try:
            sig = inspect.signature(func)
            bound = sig.bind_partial(*args, **kwargs)
            params: Dict[str, Any] = dict(bound.arguments)
        except Exception:
            params = {"args": args, "kwargs": kwargs}
        print(f"```calling {tool_name} with params: ```")
        print(f"```{_format_for_log(params)}```")
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"```{tool_name} responded:\n <raised {e.__class__.__name__}: {e}>```")
            raise
        print(f"```{tool_name} responded:\n{_format_for_log(result)}```")
        return result
    return wrapper


def _read_json(path_parts: List[str]) -> Any:
    path = os.path.join(ROOT, *path_parts)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.exception("Failed reading JSON %s", path)
        raise


def load_catalog() -> List[Dict[str, Any]]:
    return _read_json(["data", "catalog", "products.json"])  # type: ignore[no-any-return]


def load_inventory() -> List[Dict[str, Any]]:
    return _read_json(["data", "inventory", "inventory.json"])  # type: ignore[no-any-return]


# Supported destinations for demo pricing rules
SUPPORTED_DESTINATIONS: List[Dict[str, str]] = [
    {"city": "New York", "country": "US"},
    {"city": "San Francisco", "country": "US"},
    {"city": "Chicago", "country": "US"},
    {"city": "Los Angeles", "country": "US"},
    {"city": "Austin", "country": "US"},
    {"city": "Seattle", "country": "US"},
    {"city": "Boston", "country": "US"},
    {"city": "London", "country": "UK"},
    {"city": "Berlin", "country": "DE"},
    {"city": "Paris", "country": "FR"},
]


def is_supported_destination(city: Optional[str], country: Optional[str]) -> bool:
    if not city or not country:
        return False
    norm_city = city.strip().lower()
    norm_country = country.strip().upper()
    for d in SUPPORTED_DESTINATIONS:
        if d["city"].lower() == norm_city and d["country"].upper() == norm_country:
            return True
    return False


def list_supported_destinations(limit: int = 20) -> List[Dict[str, str]]:
    return SUPPORTED_DESTINATIONS[:limit]


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


def find_price_for_sku(products: List[Dict[str, Any]], sku: str) -> Optional[Dict[str, Any]]:
    for product in products:
        for variant in product.get("variants", []):
            if (variant.get("sku") or "").strip() == sku:
                return {
                    "sku": sku,
                    "unitPriceCents": int(variant.get("listPrice", 0)),
                    "currency": variant.get("currency", "USD"),
                }
    return None


_COUNTRY_NORMALIZATION = {
    "USA": "US",
    "UNITED STATES": "US",
    "U.S.": "US",
    "U S": "US",
    "US": "US",
    "UNITED KINGDOM": "UK",
    "GREAT BRITAIN": "UK",
    "UK": "UK",
    "GB": "UK",
    "GERMANY": "DE",
    "DE": "DE",
    "DEU": "DE",
    "FRANCE": "FR",
    "FR": "FR",
    "FRA": "FR",
}


def normalize_country(country: Optional[str]) -> Optional[str]:
    if not country:
        return None
    key = (country or "").strip().upper()
    return _COUNTRY_NORMALIZATION.get(key, key)


def find_sku_for_product_variant_attributes(products: List[Dict[str, Any]], product_id: str, attrs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not product_id or not attrs:
        return None
    product = _find_product_by_id(products, product_id)
    if not product:
        return None
    wanted = {str(k).strip().lower(): str(v).strip().lower() for k, v in attrs.items()}
    for v in product.get("variants", []):
        vat = {str(k).strip().lower(): str(vv).strip().lower() for k, vv in (v.get("attributes") or {}).items()}
        if all(vat.get(k) == val for k, val in wanted.items()):
            return {
                "sku": v.get("sku"),
                "unitPriceCents": int(v.get("listPrice", 0)),
                "currency": v.get("currency", "USD"),
            }
    return None


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



