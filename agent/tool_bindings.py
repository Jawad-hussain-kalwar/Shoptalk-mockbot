from typing import Any, Dict, List

from tools import (
    search_products,
    get_product_details,
    check_inventory,
    estimate_price,
    suggest_alternatives,
    create_order,
    get_order_status,
)


# Tool schema for google-generativeai function calling
TOOLS: List[Dict[str, Any]] = [
    {
        "name": "SearchProducts",
        "description": "Find products by text query and optional category.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {"type": "STRING"},
                "category": {"type": "STRING"},
                "limit": {"type": "INTEGER"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "GetProductDetails",
        "description": "Retrieve canonical details for a specific product id.",
        "parameters": {
            "type": "OBJECT",
            "properties": {"product_id": {"type": "STRING"}},
            "required": ["product_id"],
        },
    },
    {
        "name": "CheckInventory",
        "description": "Check stock and restock ETA for a given SKU.",
        "parameters": {
            "type": "OBJECT",
            "properties": {"sku": {"type": "STRING"}},
            "required": ["sku"],
        },
    },
    {
        "name": "EstimatePrice",
        "description": "Compute price estimate for items to a destination city/country.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "items": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "sku": {"type": "STRING"},
                            "unitPriceCents": {"type": "INTEGER"},
                            "quantity": {"type": "INTEGER"},
                        },
                        "required": ["sku", "unitPriceCents", "quantity"],
                    },
                },
                "destination_city": {"type": "STRING"},
                "destination_country": {"type": "STRING"},
            },
            "required": ["items"],
        },
    },
    {
        "name": "SuggestAlternatives",
        "description": "Suggest alternatives within budget for a reference product.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "reference_product_id": {"type": "STRING"},
                "max_price_cents": {"type": "INTEGER"},
                "limit": {"type": "INTEGER"},
            },
            "required": ["reference_product_id"],
        },
    },
    {
        "name": "CreateOrder",
        "description": "Create an order after explicit user confirmation.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "items": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "sku": {"type": "STRING"},
                            "quantity": {"type": "INTEGER"},
                            "unitPriceCents": {"type": "INTEGER"},
                        },
                        "required": ["sku", "quantity", "unitPriceCents"],
                    },
                },
                "destination_city": {"type": "STRING"},
                "destination_country": {"type": "STRING"},
                "breakdown": {"type": "OBJECT"},
            },
            "required": ["items", "breakdown"],
        },
    },
    {
        "name": "GetOrderStatus",
        "description": "Get current order status by id.",
        "parameters": {
            "type": "OBJECT",
            "properties": {"order_id": {"type": "STRING"}},
            "required": ["order_id"],
        },
    },
]


def call_local_tool(name: str, args: dict) -> Any:
    if name == "SearchProducts":
        return search_products(args["query"], category=args.get("category"), limit=args.get("limit", 10))
    if name == "GetProductDetails":
        return get_product_details(args["product_id"])  # may be None
    if name == "CheckInventory":
        return check_inventory(args["sku"])  # may be None
    if name == "EstimatePrice":
        return estimate_price(args["items"], destination_city=args.get("destination_city"), destination_country=args.get("destination_country"))
    if name == "SuggestAlternatives":
        return suggest_alternatives(args["reference_product_id"], max_price_cents=args.get("max_price_cents"), limit=args.get("limit", 3))
    if name == "CreateOrder":
        return create_order(items=args["items"], destination_city=args.get("destination_city"), destination_country=args.get("destination_country"), breakdown=args["breakdown"])  # may be None
    if name == "GetOrderStatus":
        return get_order_status(args["order_id"])  # may be None
    raise ValueError(f"Unknown tool: {name}")


