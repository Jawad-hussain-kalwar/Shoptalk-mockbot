import json
import sys
from typing import Any, Dict

from agent.gemini_client import GeminiClient
from agent.tool_bindings import call_local_tool


WELCOME = "Welcome to ShopTalk! Ask about products, availability, price, or orders. Type 'exit' to quit."


def _handle_tool_calls(resp: Any, chat: Any) -> Any:
    # With automatic function calling enabled by passing Python functions as tools,
    # the SDK handles calling and resuming. Just return the response.
    return resp


def run() -> None:
    print(WELCOME)
    client = GeminiClient()
    chat = client.start_chat()
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
        resp = chat.send_message(user)
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


