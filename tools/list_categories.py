from typing import List

from ._shared import load_catalog, log_tool_call


@log_tool_call
def list_categories() -> List[str]:
    products = load_catalog()
    cats = sorted({(p.get("category") or "").strip() for p in products if p.get("category")})
    return cats


