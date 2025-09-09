import json

from agent.gemini_client import GeminiClient
from agent.system_prompt import SYSTEM_PROMPT
from agent.logging_config import init_logging
from google.genai import types, errors
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


WELCOME = (
    "Welcome to ShopTalk! Ask about products, availability, price, or orders. Type 'exit' to quit."
)


def run() -> None:
    """Run the REPL that powers the multi-turn conversational agent.

    This function wires the Gemini chat session with the available Python
    tool functions. The model decides when to call tools based on the
    provided type hints and docstrings.
    """
    print(WELCOME)  # Tell the user what this demo does and how to exit
    init_logging()  # Create a file logger so we can inspect behavior after runs
    client = GeminiClient()  # Create an API client using the GEMINI_API_KEY from environment
    chat = client.start_chat()  # Start a persistent chat so the model remembers context across turns

    # Tools are regular Python functions the model can call to fetch real data or perform actions
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

    # This configuration is sent with each turn so behavior is consistent and guarded by a system prompt
    common_config = types.GenerateContentConfig(
        tools=tool_functions,  # Give the model the toolbox so it can function-call when needed
        system_instruction=SYSTEM_PROMPT,  # High-level role/guardrails so outputs stay on-task and safe
    )

    # The REPL (read–eval–print loop) keeps asking for input and sending it to the chat session
    while True:
        try:
            user = input("> ").strip()  # Read input from the terminal and trim whitespace
        except (EOFError, KeyboardInterrupt):
            print()
            break  # Gracefully exit on Ctrl+D/Ctrl+C so the demo stops cleanly
        if user.lower() in {"exit", "quit"}:  # Provide a clear exit command for new users
            break
        if not user:
            continue  # Ignore empty inputs to avoid accidental tool calls
        try:
            # Send a new user turn; the model may plan and call tools automatically
            resp = chat.send_message(user, config=common_config)
        except errors.APIError as e:
            print(f"[APIError] {getattr(e, 'message', str(e))}")  # Surface API issues without crashing the REPL
            continue
        except Exception as e:
            print(f"[Error] {e}")  # Catch-all to keep the teaching demo resilient
            continue
        try:
            # Most responses include a final text; we prefer that for human readability
            text = resp.text  # type: ignore[attr-defined]
        except Exception:
            # If text is unavailable, print a JSON view so learners can inspect raw structures
            text = json.dumps(resp.to_dict() if hasattr(resp, "to_dict") else str(resp))
        print(text)  # Show the model's answer (and any tool summaries emitted by tools)


