from typing import Dict, Optional

from ._shared import load_catalog, find_price_for_sku, log_tool_call


@log_tool_call
def get_price_for_sku(sku: str) -> Optional[Dict[str, object]]:
    """Return price and currency information for a SKU, if found.

    Args:
        sku: Variant SKU identifier.

    Returns:
        Dict with unitPriceCents and currency if found, else None.
    """
    products = load_catalog()
    return find_price_for_sku(products, sku)


