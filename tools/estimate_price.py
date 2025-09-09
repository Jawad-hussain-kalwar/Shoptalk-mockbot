from typing import Any, Dict, List, Optional, Tuple
import logging

from ._shared import (
    PriceBreakdown,
    normalize_country,
    find_price_for_sku,
    find_sku_for_product_variant_attributes,
    load_catalog,
    log_tool_call,
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


@log_tool_call
def estimate_price(
    items: list[dict],
    *,
    destination_city: str,
    destination_country: str,
) -> dict:
    """
    Compute a price estimate for a cart to a destination.

    Parameters (the model must fill exactly this structure):
    - items: array of objects. Each item MUST include:
      - quantity: integer >= 1
      And include ONE of the following ways to specify the product:
      (A) sku: string (preferred). Price is auto-looked-up.
      (B) unitPriceCents: integer (fallback) if sku is not known.
      (C) productId + attributes: object; when provided, I will infer sku and price.

      Examples:
      [{"sku": "HP-AUR-100-BLK", "quantity": 1}]
      [{"productId": "hp-aurora-100", "attributes": {"color": "Black"}, "quantity": 1}]

    - destination_city: string (e.g., "New York") REQUIRED
    - destination_country: string (e.g., "US", "UK", "DE", "FR") REQUIRED. I will normalize common variants (e.g., "USA" -> "US").

    Returns: object
      On success:
        {
          items: [{sku, unitPriceCents, currency, quantity}],
          destinationCity: string,
          destinationCountry: string,
          breakdown: {subtotalCents, discountCents, taxCents, shippingCents, totalCents, subtotal, discount, tax, shipping, total},
          deliveryEtaDays: [minDays, maxDays]
        }
      On error:
        { error: string, invalidItems?: [ {item, reason} ] }
    """
    logger = logging.getLogger(__name__)
    try:
        # Validate destination
        if not destination_city or not destination_country:
            return {"error": "Missing destination_city or destination_country"}

        if not isinstance(items, list) or not items:
            logger.warning("estimate_price: empty or invalid items: %s", items)
            return {"error": "No items provided"}

        destination_country = normalize_country(destination_country)

        subtotal = 0
        total_qty = 0
        products = load_catalog()
        normalized_items: List[Dict[str, Any]] = []
        invalid_items: List[Dict[str, Any]] = []

        for item in items:
            try:
                qty = int(item.get("quantity", 1))
                if qty <= 0:
                    invalid_items.append({"item": item, "reason": "quantity must be >= 1"})
                    continue
                price = int(item.get("unitPriceCents", 0))
                sku = (item.get("sku") or "").strip() if item.get("sku") else None

                # If only product/attributes provided, try to resolve a sku
                if not sku and item.get("productId") and item.get("attributes"):
                    resolved = find_sku_for_product_variant_attributes(
                        products, str(item.get("productId")), dict(item.get("attributes"))
                    )
                    if resolved:
                        sku = str(resolved.get("sku"))
                        if price <= 0:
                            price = int(resolved.get("unitPriceCents", 0))

                # If sku present but price missing, look up price
                if (price <= 0) and sku:
                    found = find_price_for_sku(products, sku)
                    if found:
                        price = int(found.get("unitPriceCents", 0))
                        currency = found.get("currency", "USD")
                    else:
                        currency = "USD"
                else:
                    currency = "USD"

                # If still no price, skip this item
                if price <= 0:
                    invalid_items.append({"item": item, "reason": "missing price and sku could not be resolved"})
                    continue

                subtotal += qty * price
                total_qty += qty
                normalized_items.append({"sku": sku, "unitPriceCents": price, "currency": currency, "quantity": qty})
            except Exception:
                logger.exception("estimate_price: error processing item: %s", item)
                invalid_items.append({"item": item, "reason": "exception while processing item"})
                continue

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

        if not normalized_items:
            logger.warning("estimate_price: no valid items after normalization: %s", items)
            return {"error": "No valid items with prices", "invalidItems": invalid_items}

        result = {
            "items": normalized_items,
            "destinationCity": destination_city,
            "destinationCountry": destination_country,
            "breakdown": breakdown.to_dict(),
            "deliveryEtaDays": [eta_days_min, eta_days_max],
        }
        if invalid_items:
            result["invalidItems"] = invalid_items
        logger.info("estimate_price: success: %s", result)
        return result
    except Exception as e:
        logger.exception(
            "estimate_price: failed with inputs items=%s dest_city=%s dest_country=%s",
            items,
            destination_city,
            destination_country,
        )
        return {"error": str(e)}


