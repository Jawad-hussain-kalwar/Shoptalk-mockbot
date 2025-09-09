from typing import Dict, Optional

from ._shared import is_supported_destination, log_tool_call


@log_tool_call
def validate_destination(city: Optional[str], country: Optional[str]) -> Dict[str, object]:
    """Validate whether a destination city/country is supported.

    Args:
        city: Destination city name.
        country: Destination country code or name.

    Returns:
        Dict with keys: ok (bool), normalized (city/country), and optional hint string.
    """
    ok = is_supported_destination(city, country)
    return {
        "ok": ok,
        "normalized": {
            "city": (city or "").strip() if city else None,
            "country": (country or "").strip().upper() if country else None,
        },
        "hint": None if ok else "Use list_supported_destinations to see examples (e.g., New York, US)",
    }


