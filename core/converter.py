"""
Pure business logic for JSON, YAML, and tabular data conversion.
Zero Streamlit or UI dependencies.
"""

import json
from typing import Dict, Any, Tuple


def convert_and_format_json(raw_text: str, indent: int = 2, sort_keys: bool = False) -> Tuple[bool, str, Dict[str, Any]]:
    """Validates, prettifies, and calculates metrics for JSON strings."""
    if not raw_text or not raw_text.strip():
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


def minify_json(raw_text: str) -> Tuple[bool, str, Dict[str, Any]]:
    """Minifies JSON text into compact single-line representation."""
    if not raw_text or not raw_text.strip():
        return False, "Input is empty.", {}

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as err:
        return False, f"JSON Syntax Error: {err.msg}", {}

    minified = json.dumps(parsed, separators=(",", ":"))
    original_size = len(raw_text.encode("utf-8"))
    minified_size = len(minified.encode("utf-8"))
    savings = max(0, original_size - minified_size)
    ratio = (savings / original_size * 100) if original_size > 0 else 0.0

    metrics = {
        "original_bytes": original_size,
        "minified_bytes": minified_size,
        "bytes_saved": savings,
        "compression_percentage": f"{round(ratio, 1)}%",
    }
    return True, minified, metrics


def flatten_json(data: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flattens a nested dictionary into dot-notation key-value pairs."""
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    elif isinstance(data, list):
        for idx, v in enumerate(data):
            new_key = f"{parent_key}[{idx}]" if parent_key else f"[{idx}]"
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, data))
    return dict(items)
