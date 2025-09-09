import os
from typing import Any

from dotenv import load_dotenv
from google import genai


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


