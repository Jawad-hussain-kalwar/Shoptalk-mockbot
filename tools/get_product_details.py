from typing import Any, Dict, Optional

from ._shared import load_catalog, _find_product_by_id, log_tool_call


@log_tool_call
def get_product_details(product_id: str) -> Optional[Dict[str, Any]]:
    """Return full product details by product id.

    Args:
        product_id: The canonical id of the product.

    Returns:
        The product object from the catalog, or None if not found.
    """
    products = load_catalog()
    product = _find_product_by_id(products, product_id)
    if not product:
        return None
    return product


