from typing import Any, Dict, List

from ._shared import load_catalog, log_tool_call


@log_tool_call
def list_products(*, limit: int = 20) -> List[Dict[str, Any]]:
    products = load_catalog()
    results: List[Dict[str, Any]] = []
    for p in products[:limit]:
        results.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "category": p.get("category"),
            "shortDescription": p.get("shortDescription"),
            "tags": p.get("tags", []),
        })
    return results


