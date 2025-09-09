from typing import Any, Dict, List

from ._shared import load_catalog, log_tool_call


def _matches(product: Dict[str, Any], query: str, tags: List[str]) -> bool:
    q = query.lower().strip()
    hay = " ".join([
        product.get("name", ""),
        product.get("category", ""),
        product.get("shortDescription", ""),
        " ".join(tags),
    ]).lower()
    return all(part in hay for part in q.split())


@log_tool_call
def search_products(query: str, *, category: str | None = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Search products by free-text query, optionally filtered by category.

    Args:
        query: Free-text search string; matches name, category, description, and tags.
        category: Optional category name to restrict results.
        limit: Maximum number of products to return.

    Returns:
        A list of product summaries including id, name, category, shortDescription,
        tags, and basic variant info.
    """
    products = load_catalog()
    results: List[Dict[str, Any]] = []
    for p in products:
        if category and p.get("category") != category:
            continue
        tags = p.get("tags", [])
        if _matches(p, query, tags):
            results.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "category": p.get("category"),
                "shortDescription": p.get("shortDescription"),
                "tags": tags,
                "variants": [{"sku": v.get("sku"), "attributes": v.get("attributes"), "listPrice": v.get("listPrice"), "currency": v.get("currency")} for v in p.get("variants", [])],
            })
            if len(results) >= limit:
                break
    return results


