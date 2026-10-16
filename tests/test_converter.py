"""
Unit tests for suite-data-convert business logic.
"""

import sys
import unittest
from pathlib import Path

# Ensure suite root is in sys.path
SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.converter import convert_and_format_json


class TestConverter(unittest.TestCase):
    def test_valid_json_formatting(self):
        raw = '{"name":"DeveloperOS","version":1}'
        success, formatted, metrics = convert_and_format_json(raw, indent=2)
        self.assertTrue(success)
        self.assertIn('"name": "DeveloperOS"', formatted)
        self.assertEqual(metrics["item_count"], 2)
        self.assertTrue(metrics["is_object"])

    def test_invalid_json_handling(self):
        raw = '{"name": DeveloperOS}'  # Missing quotes
        success, err_msg, metrics = convert_and_format_json(raw)
        self.assertFalse(success)
        self.assertIn("JSON Syntax Error", err_msg)
        self.assertEqual(metrics, {})


if __name__ == "__main__":
    unittest.main()
