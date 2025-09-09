from typing import Dict, Optional

from ._shared import load_catalog, find_price_for_sku, log_tool_call


@log_tool_call
def get_price_for_sku(sku: str) -> Optional[Dict[str, object]]:
    products = load_catalog()
    return find_price_for_sku(products, sku)


