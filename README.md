# ShopTalk (Gemini + Tools)

A concise terminal shopping assistant powered by Google GenAI (Gemini) with local tool functions for catalog search, product details, inventory checks, price estimation, and basic order flow.

## Prerequisites
- Python 3.11+
- `GEMINI_API_KEY` set in your environment (Google AI Studio API key)
- Virtual environment recommended

## Setup
```bash
# From repo root
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -U pip
pip install -r requirements.txt
```

Optionally create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

## Run
```bash
python main.py
```
You’ll see a welcome message. Try:
- "search headphones"
- "show details for <product_id>"
- "check inventory for <sku>"
- "estimate price to <city>, <country>"
- "create order" (after explicit confirmation and a valid estimate)

Type `exit` to quit.

## Project Structure
- `agent/gemini_client.py`: Creates a `genai.Client` chat for Gemini models.
- `main.py`: CLI loop; configures tools for automatic function calling per message.
- `tools/`: Local tool functions (catalog search, details, inventory, pricing, order, status).
- `data/`: Mock data used by tools.
- `docs/AGENT_PLAN.md`: Agent loop plan.
- `PRD.md`: Product requirements/design notes.

## Notes
- Uses `google-genai` SDK. Tools are passed as Python callables via `GenerateContentConfig(tools=[...])`.
- Guardrail: no order is placed without an estimate and explicit user confirmation.

## Environment
- See `ENV.md` for environment details.
