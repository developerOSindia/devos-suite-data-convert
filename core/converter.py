"""
Pure business logic for JSON, YAML, and tabular data conversion.
Zero Streamlit or UI dependencies.
"""

import json
from typing import Dict, Any, Tuple


def convert_and_format_json(raw_text: str, indent: int = 2, sort_keys: bool = False) -> Tuple[bool, str, Dict[str, Any]]:
    """Validates, prettifies, and calculates metrics for JSON strings."""
    if not raw_text.strip():
        return False, "Input is empty.", {}

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as err:
        return False, f"JSON Syntax Error on line {err.lineno}, col {err.colno}: {err.msg}", {}

    formatted = json.dumps(parsed, indent=indent, sort_keys=sort_keys)
    
    # Calculate structure metrics
    metrics = {
        "byte_size": len(formatted.encode("utf-8")),
        "is_array": isinstance(parsed, list),
        "is_object": isinstance(parsed, dict),
        "item_count": len(parsed) if isinstance(parsed, (list, dict)) else 1,
    }

    return True, formatted, metrics
