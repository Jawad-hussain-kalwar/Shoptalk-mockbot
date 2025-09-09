import json
import os
import time
import uuid
import logging
from typing import Any, Dict, List

from ._shared import ROOT, log_tool_call


ORDERS_PATH = os.path.join(ROOT, "data", "orders", "orders.json")


def _read_orders() -> List[Dict[str, Any]]:
    if not os.path.exists(ORDERS_PATH):
        return []
    with open(ORDERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_orders(rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(ORDERS_PATH), exist_ok=True)
    try:
        with open(ORDERS_PATH, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
    except Exception:
        logging.exception("Failed writing orders JSON: %s", ORDERS_PATH)
        raise


@log_tool_call
def create_order(*, items: list[dict], destination_city: str, destination_country: str, breakdown: dict) -> dict | None:
    """Create and persist a simple demo order in the local JSON store.

    Args:
        items: Normalized items with sku, unitPriceCents, currency, quantity.
        destination_city: Shipping city.
        destination_country: Shipping country code.
        breakdown: Price breakdown used for the order record.

    Returns:
        A dict with orderId and status if created; otherwise None.
    """
    if not items:
        return None

    order_id = str(uuid.uuid4())[:8]
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    row = {
        "orderId": order_id,
        "items": items,
        "destinationCity": destination_city,
        "destinationCountry": destination_country,
        "breakdown": breakdown,
        "status": "received",
        "createdAt": now_iso,
    }

    orders = _read_orders()
    orders.append(row)
    _write_orders(orders)

    return {"orderId": order_id, "status": "received"}


