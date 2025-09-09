import json
import os
from typing import Any, Dict, Optional

from ._shared import ROOT


ORDERS_PATH = os.path.join(ROOT, "data", "orders", "orders.json")


def get_order_status(order_id: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(ORDERS_PATH):
        return None
    with open(ORDERS_PATH, "r", encoding="utf-8") as f:
        rows = json.load(f)
    for row in rows:
        if row.get("orderId") == order_id:
            return {"orderId": order_id, "status": row.get("status"), "createdAt": row.get("createdAt")}
    return None


