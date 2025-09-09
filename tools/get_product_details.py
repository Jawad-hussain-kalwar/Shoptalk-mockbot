from typing import Any, Dict, Optional

from ._shared import load_catalog, _find_product_by_id


def get_product_details(product_id: str) -> Optional[Dict[str, Any]]:
    products = load_catalog()
    product = _find_product_by_id(products, product_id)
    if not product:
        return None
    return product


