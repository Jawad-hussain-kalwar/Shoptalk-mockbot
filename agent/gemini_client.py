import os
from typing import Any

from dotenv import load_dotenv
import google.generativeai as genai
from tools import (
    search_products,
    get_product_details,
    check_inventory,
    estimate_price,
    suggest_alternatives,
    create_order,
    get_order_status,
)


SYSTEM_PROMPT = (
    "You are ShopTalk, a concise shopping assistant. Always be brief and clear. "
    "Use tools when needed. Do not place an order unless the user confirms after an estimate."
)


class GeminiClient:
    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(
            model_name,
            tools=[
                search_products,
                get_product_details,
                check_inventory,
                estimate_price,
                suggest_alternatives,
                create_order,
                get_order_status,
            ],
            system_instruction=SYSTEM_PROMPT,
        )

    def start_chat(self) -> Any:
        return self._model.start_chat(history=[])


