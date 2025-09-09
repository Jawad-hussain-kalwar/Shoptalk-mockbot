import os
from typing import Any

from dotenv import load_dotenv
from google import genai


class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.0-flash-001") -> None:
        """Create a thin client wrapper around google-genai.

        - Loads `GEMINI_API_KEY` from environment (via .env for local dev).
        - Instantiates `genai.Client()` used for chats and content generation.
        - Stores the chosen model name for chat sessions.
        """
        load_dotenv()  # Support local development by loading .env automatically
        api_key = os.getenv("GEMINI_API_KEY")  # Keep secrets out of code by using environment variables
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")  # Fail fast with a clear error if missing
        # Construct a single client to reuse connections and settings across calls
        # The google-genai Client auto-reads GEMINI_API_KEY from the environment
        self._client = genai.Client()
        # Choose the default model; faster Flash is good for interactive demos
        self._model_name = model_name

    def start_chat(self) -> Any:
        """Start a multi-turn chat session with the configured model."""
        # A chat keeps context across turns so the model can remember prior messages
        return self._client.chats.create(model=self._model_name)


