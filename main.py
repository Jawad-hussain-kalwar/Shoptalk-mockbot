import json
import sys
from typing import Any, Dict

from agent.gemini_client import GeminiClient
from agent.system_prompt import SYSTEM_PROMPT
from agent.logging_config import init_logging
from google.genai import types
from tools import (
    search_products,
    get_product_details,
    check_inventory,
    estimate_price,
    suggest_alternatives,
    create_order,
    get_order_status,
    list_supported_destinations,
    validate_destination,
    list_categories,
    list_products_by_category,
    list_products,
    list_products_count,
    list_variants,
    validate_sku,
    get_price_for_sku,
)


WELCOME = "Welcome to ShopTalk! Ask about products, availability, price, or orders. Type 'exit' to quit."


def _handle_tool_calls(resp: Any, chat: Any) -> Any:
    # With automatic function calling enabled by passing Python functions as tools,
    # the SDK handles calling and resuming. Just return the response.
    return resp


def run() -> None:
    print(WELCOME)
    init_logging()
    client = GeminiClient()
    chat = client.start_chat()
    tool_functions = [
        search_products,
        get_product_details,
        check_inventory,
        estimate_price,
        suggest_alternatives,
        create_order,
        get_order_status,
        list_supported_destinations,
        validate_destination,
        list_categories,
        list_products_by_category,
        list_products,
        list_products_count,
        list_variants,
        validate_sku,
        get_price_for_sku,
    ]
    common_config = types.GenerateContentConfig(
        tools=tool_functions,
        # Enforce our guardrail via system instruction each turn.
        system_instruction=SYSTEM_PROMPT,
    )
    while True:
        try:
            user = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user.lower() in {"exit", "quit"}:
            break
        if not user:
            continue
        resp = chat.send_message(user, config=common_config)
        resp = _handle_tool_calls(resp, chat)
        # Print final text
        try:
            text = resp.text  # type: ignore[attr-defined]
        except Exception:
            # Fallback: raw
            text = json.dumps(resp.to_dict() if hasattr(resp, "to_dict") else str(resp))
        print(text)


if __name__ == "__main__":
    run()


