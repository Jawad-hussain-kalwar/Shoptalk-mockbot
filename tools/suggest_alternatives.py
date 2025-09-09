from typing import Any, Dict, List, Optional

from ._shared import load_catalog, log_tool_call


@log_tool_call
def suggest_alternatives(reference_product_id: str, *, max_price_cents: int | None = None, limit: int = 3) -> List[Dict[str, Any]]:
    """Suggest similar products, preferring same category and within budget if set.

    Args:
        reference_product_id: Product id to find alternatives for.
        max_price_cents: Optional max unit price threshold for variants.
        limit: Maximum number of alternatives to return.

    Returns:
        A list of alternative product summaries with a representative variant.
    """
    products = load_catalog()
    results: List[Dict[str, Any]] = []
    ref = next((p for p in products if p.get("id") == reference_product_id), None)
    ref_category = ref.get("category") if ref else None

    for p in products:
        if p.get("id") == reference_product_id:
            continue
        # Prefer same category
        if ref_category and p.get("category") != ref_category:
            continue
        # Price filter: include if any variant within budget
        variants = p.get("variants", [])
        if max_price_cents is not None:
            if not any(int(v.get("listPrice", 0)) <= max_price_cents for v in variants):
                continue
        # Pick the cheapest variant as representative
        cheapest = min(variants, key=lambda v: int(v.get("listPrice", 0)), default=None)
        results.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "category": p.get("category"),
            "shortDescription": p.get("shortDescription"),
            "representativeSku": cheapest.get("sku") if cheapest else None,
            "representativePrice": cheapest.get("listPrice") if cheapest else None,
            "currency": cheapest.get("currency") if cheapest else None,
            "tags": p.get("tags", []),
        })
        if len(results) >= limit:
            break

    return results


