from typing import Any, Dict, List

from ._shared import _find_product_by_id, load_catalog, log_tool_call


@log_tool_call
def list_variants(product_id: str) -> List[Dict[str, Any]]:
    """List variant SKUs and attributes for a product.

    Args:
        product_id: The product id to enumerate variants for.

    Returns:
        A list of variants with sku, attributes, listPrice, and currency.
    """
    products = load_catalog()
    product = _find_product_by_id(products, product_id)
    if not product:
        return []
    out: List[Dict[str, Any]] = []
    for v in product.get("variants", []):
        out.append({
            "sku": v.get("sku"),
            "attributes": v.get("attributes"),
            "listPrice": int(v.get("listPrice", 0)),
            "currency": v.get("currency", "USD"),
        })
    return out


