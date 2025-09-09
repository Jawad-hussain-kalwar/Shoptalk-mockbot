from typing import Any, Dict, List

from ._shared import load_catalog, log_tool_call


@log_tool_call
def list_products_by_category(category: str, *, limit: int = 20) -> List[Dict[str, Any]]:
    """List products within a specific category.

    Args:
        category: Category name to filter by.
        limit: Maximum number of products to return.

    Returns:
        A list of product summaries within the category.
    """
    products = load_catalog()
    results: List[Dict[str, Any]] = []
    for p in products:
        if (p.get("category") or "").strip().lower() == (category or "").strip().lower():
            results.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "category": p.get("category"),
                "shortDescription": p.get("shortDescription"),
                "tags": p.get("tags", []),
            })
            if len(results) >= limit:
                break
    return results


