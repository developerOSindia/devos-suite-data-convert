"""
Unit tests for suite-data-convert business logic.
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.converter import convert_and_format_json, minify_json, flatten_json


class TestConverter(unittest.TestCase):
    def test_valid_json_formatting(self):
        raw = '{"name": "DeveloperOS", "version": 1, "active": true}'
        ok, res, metrics = convert_and_format_json(raw, indent=2)
        self.assertTrue(ok)
        self.assertIn('"name": "DeveloperOS"', res)
        self.assertEqual(metrics["item_count"], 3)
        self.assertTrue(metrics["is_object"])

    def test_invalid_json(self):
        raw = '{name: broken_json}'
        ok, err_msg, metrics = convert_and_format_json(raw)
        self.assertFalse(ok)
        self.assertIn("JSON Syntax Error", err_msg)
        self.assertEqual(metrics, {})

    def test_empty_json(self):
        ok, err_msg, metrics = convert_and_format_json("   ")
        self.assertFalse(ok)
        self.assertEqual(err_msg, "Input is empty.")

    def test_none_input(self):
        ok, err_msg, metrics = convert_and_format_json(None)
        self.assertFalse(ok)
        self.assertEqual(err_msg, "Input is empty.")

    def test_minify_json(self):
        pretty = """
        {
            "tools": ["json", "jwt", "base64"],
            "count": 3
        }
        """
        ok, minified, metrics = minify_json(pretty)
        self.assertTrue(ok)
        self.assertEqual(minified, '{"tools":["json","jwt","base64"],"count":3}')
        self.assertGreater(metrics["bytes_saved"], 0)

    def test_minify_invalid_json(self):
        ok, err, metrics = minify_json("{broken")
        self.assertFalse(ok)
        self.assertIn("JSON Syntax Error", err)

    def test_flatten_nested_json(self):
        nested = {
            "app": {
                "name": "DeveloperOS",
                "settings": {
                    "theme": "dark",
                    "telemetry": False
                }
            },
            "ports": [80, 443]
        }
        flat = flatten_json(nested)
        self.assertEqual(flat["app.name"], "DeveloperOS")
        self.assertEqual(flat["app.settings.theme"], "dark")
        self.assertEqual(flat["app.settings.telemetry"], False)
        self.assertEqual(flat["ports[0]"], 80)
        self.assertEqual(flat["ports[1]"], 443)


if __name__ == "__main__":
    unittest.main()
