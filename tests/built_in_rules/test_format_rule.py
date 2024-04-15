"""FormatRule test"""

from dictrule.built_in_rules import FormatRule
import unittest


class TestFormatRule(unittest.TestCase):
    """Test class"""

    def test_format_lowercase(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_lowercase": "TEXT 123",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text 123")

    def test_format_uppercase(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_uppercase": "text 123",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "TEXT 123")

    def test_format_upper_head(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_upper_head": "myText 123",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "MyText 123")

    def test_format_empty(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_uppercase": "",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "")

    def test_format_invalid(self):
        """Test method"""

        rule = FormatRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "format_123": "text",
                },
                rule_callback=lambda x, y: y,
            )

    def test_format_none(self):
        """Test method"""

        rule = FormatRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "format_uppercase": None,
                },
                rule_callback=lambda x, y: y,
            )


if __name__ == "__main__":
    unittest.main()
