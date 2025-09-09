from typing import Dict, List

from ._shared import list_supported_destinations as _list, log_tool_call


@log_tool_call
def list_supported_destinations(limit: int = 20) -> List[Dict[str, str]]:
    """Return example supported destinations for shipping/pricing logic.

    Args:
        limit: Maximum number of destinations to return.

    Returns:
        A list of {city, country} objects.
    """
    return _list(limit=limit)


