from typing import Dict, List

from ._shared import list_supported_destinations as _list, log_tool_call


@log_tool_call
def list_supported_destinations(limit: int = 20) -> List[Dict[str, str]]:
    return _list(limit=limit)


