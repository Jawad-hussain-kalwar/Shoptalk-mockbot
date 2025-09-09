from typing import Any, Dict, List, Optional

from ._shared import load_inventory, _inventory_index_by_sku


def check_inventory(sku: str) -> Optional[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = load_inventory()
    idx = _inventory_index_by_sku(rows)
    row = idx.get(sku)
    if row is None:
        return None
    return {
        "sku": row["sku"],
        "stock": int(row.get("stock", 0)),
        "restockEtaDays": row.get("restockEtaDays"),
        "availability": "in_stock" if int(row.get("stock", 0)) > 0 else "out_of_stock",
    }


