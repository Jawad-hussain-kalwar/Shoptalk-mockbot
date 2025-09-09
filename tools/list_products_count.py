from typing import Dict

from ._shared import load_catalog, log_tool_call


@log_tool_call
def list_products_count() -> Dict[str, int]:
    products = load_catalog()
    return {"count": len(products)}


