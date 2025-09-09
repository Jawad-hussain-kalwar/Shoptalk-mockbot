from typing import Dict

from ._shared import load_catalog, log_tool_call


@log_tool_call
def validate_sku(sku: str) -> Dict[str, object]:
    products = load_catalog()
    sku_norm = (sku or "").strip()
    found = False
    for p in products:
        for v in p.get("variants", []):
            if (v.get("sku") or "").strip() == sku_norm:
                found = True
                break
        if found:
            break
    return {"ok": found, "sku": sku_norm}


