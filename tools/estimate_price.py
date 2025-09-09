from typing import Any, Dict, List, Optional

from ._shared import (
    PriceBreakdown,
)


def _calc_discount(subtotal_cents: int, destination_country: str | None) -> int:
    # Mock: 5% discount for orders shipping within "US"; otherwise 0.
    if destination_country and destination_country.upper() == "US":
        return int(round(subtotal_cents * 0.05))
    return 0


def _calc_tax(subtotal_after_discount_cents: int, destination_country: str | None) -> int:
    # Mock: 8% tax if destination is "US"; 0 otherwise.
    if destination_country and destination_country.upper() == "US":
        return int(round(subtotal_after_discount_cents * 0.08))
    return 0


def _calc_shipping(items_count: int, destination_country: str | None) -> int:
    # Mock: base 700 cents domestic, 1500 cents international; +200 per extra item.
    if destination_country and destination_country.upper() == "US":
        base = 700
    else:
        base = 1500
    extra = max(0, items_count - 1) * 200
    return base + extra


def estimate_price(items: List[Dict[str, Any]], *, destination_city: str | None = None, destination_country: str | None = None) -> Optional[Dict[str, Any]]:
    """
    items: [{"sku": str, "unitPriceCents": int, "quantity": int}]
    Returns breakdown and delivery eta window (mocked).
    """
    if not items:
        return None

    subtotal = 0
    total_qty = 0
    for item in items:
        qty = int(item.get("quantity", 1))
        price = int(item.get("unitPriceCents", 0))
        subtotal += qty * price
        total_qty += qty

    discount = _calc_discount(subtotal, destination_country)
    taxed_base = subtotal - discount
    tax = _calc_tax(taxed_base, destination_country)
    shipping = _calc_shipping(total_qty, destination_country)
    total = taxed_base + tax + shipping

    breakdown = PriceBreakdown(
        subtotal_cents=subtotal,
        discount_cents=discount,
        tax_cents=tax,
        shipping_cents=shipping,
        total_cents=total,
    )

    eta_days_min = 2 if (destination_country or "").upper() == "US" else 5
    eta_days_max = 5 if (destination_country or "").upper() == "US" else 12

    return {
        "items": items,
        "destinationCity": destination_city,
        "destinationCountry": destination_country,
        "breakdown": breakdown.to_dict(),
        "deliveryEtaDays": [eta_days_min, eta_days_max],
    }


