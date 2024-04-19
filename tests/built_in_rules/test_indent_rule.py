"""IndentRule test"""

import unittest
from dictrule.context import Context
from dictrule.built_in_rules import IndentRule
from dictrule.exceptions import (
    NoneValueException,
    InvalidTypeException,
)


class NotIndentCase(Context.Case):
    """Test class"""

    @property
    def name(self) -> str:
        return IndentRule.CONTEXT_NAME


class TestIndentRule(unittest.TestCase):
    """Test class"""

    def test_indent_1(self):
        """Test method"""

        rule = IndentRule()

        parsed = rule.parse(
            rule_dict={"indent_1": "indent-1"},
            context=Context([IndentRule.ContextCase(2)]),
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, " " * 2 + "indent-1")

    def test_indent_10(self):
        """Test method"""

        rule = IndentRule()

        parsed = rule.parse(
            rule_dict={"indent_10": "indent-10"},
            context=Context([IndentRule.ContextCase(4)]),
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, " " * 4 * 10 + "indent-10")

    def test_none_context(self):
        """Test method"""

        rule = IndentRule()

        with self.assertRaises(NoneValueException):
            _ = rule.parse(
                rule_dict={"indent_1": "indent-1"},
                context=None,
                rule_callback=lambda x, y: y,
            )

    def test_none_context_case(self):
        """Test method"""

        rule = IndentRule()

        with self.assertRaises(InvalidTypeException):
            _ = rule.parse(
                rule_dict={"indent_1": "indent-1"},
                context=Context([NotIndentCase()]),
                rule_callback=lambda x, y: y,
            )

    def test_indent_none(self):
        """Test method"""

        rule = IndentRule()

        parsed = rule.parse(
            rule_dict={
                "indent_10": None,
            },
            context=Context([IndentRule.ContextCase(4)]),
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, " " * 4 * 10 + "")

    def test_indent_str(self):
        """Test method"""

        rule = IndentRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "indent_abc": "test",
                },
                context=Context([IndentRule.ContextCase(4)]),
                rule_callback=lambda x, y: y if y else "",
            )

    def test_indent_invalid_value_context(self):
        """Test method"""

        rule = IndentRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "indent_abc": "test",
                },
                context=Context([IndentRule.ContextCase(2)]),
                rule_callback=lambda x, y: y if y else "",
            )

    def test_indent_neg_space_context(self):
        """Test method"""

        rule = IndentRule()

        parsed = rule.parse(
            rule_dict={
                "indent_2": "test",
            },
            context=Context([IndentRule.ContextCase(2)]),
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, " " * IndentRule.DEFAULT_SPACES * 2 + "test")

    def test_indent_empty_context(self):
        """Test method"""

        rule = IndentRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "indent_abc": "test",
                },
                context=Context([]),
                rule_callback=lambda x, y: y if y else "",
            )


if __name__ == "__main__":
    unittest.main()
