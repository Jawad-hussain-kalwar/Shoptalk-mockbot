import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

from ._shared import ROOT, PriceBreakdown


ORDERS_PATH = os.path.join(ROOT, "data", "orders", "orders.json")


def _read_orders() -> List[Dict[str, Any]]:
    if not os.path.exists(ORDERS_PATH):
        return []
    with open(ORDERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_orders(rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(ORDERS_PATH), exist_ok=True)
    with open(ORDERS_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def create_order(*, items: List[Dict[str, Any]], destination_city: str | None, destination_country: str | None, breakdown: Dict[str, Any]) -> Optional[Dict[str, Any]]:
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


