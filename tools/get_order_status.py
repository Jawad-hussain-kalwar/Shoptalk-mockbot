import json
import os
from typing import Any, Dict, Optional

from ._shared import ROOT, log_tool_call


ORDERS_PATH = os.path.join(ROOT, "data", "orders", "orders.json")


@log_tool_call
def get_order_status(order_id: str) -> Optional[Dict[str, Any]]:
    """Look up an order status by id from the local JSON store.

    Args:
        order_id: Short order id string.

    Returns:
        Dict with orderId, status, and createdAt; or None if not found.
    """
    if not os.path.exists(ORDERS_PATH):
        return None
    with open(ORDERS_PATH, "r", encoding="utf-8") as f:
        rows = json.load(f)
    for row in rows:
        if row.get("orderId") == order_id:
            return {"orderId": order_id, "status": row.get("status"), "createdAt": row.get("createdAt")}
    return None


