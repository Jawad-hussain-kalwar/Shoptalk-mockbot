import os
from typing import Any

from dotenv import load_dotenv
from google import genai


SYSTEM_PROMPT = (
    "You are ShopTalk, a concise shopping assistant. Always be brief and clear. "
    "Use tools when needed. Do not place an order unless the user confirms after an estimate."
)


class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.0-flash-001") -> None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        # The google-genai Client reads GEMINI_API_KEY from the environment.
        self._client = genai.Client()
        self._model_name = model_name

    def start_chat(self) -> Any:
        return self._client.chats.create(model=self._model_name)


