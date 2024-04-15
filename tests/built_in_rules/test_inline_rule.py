"""InlineRule test"""

from typing import (
    Dict,
    Any,
    Union,
    Optional,
)
import unittest
from dictrule.context import Context
from dictrule.built_in_rules import InlineRule


class TestInlineRule(unittest.TestCase):
    """Test class"""

    @staticmethod
    def _rule_callback(
        context: Optional[Context],
        rule: Union[str, Dict[str, Any]],
    ) -> str:
        _ = context
        if not rule:
            return ""

        if isinstance(rule, str):
            return rule

        eval_rule = rule.get("eval")
        if eval_rule:
            return "eval_1"

        print_rule = rule.get("print")
        if print_rule:
            return "print_2"

        log = rule.get("log")
        if log:
            return "log_3"

        return ""

    def test_inline_str(self):
        """Test method"""

        rule = InlineRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={"inline": "inline-1"},
                rule_callback=lambda x, y: y,
            )

    def test_inline_none(self):
        """Test method"""

        rule = InlineRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "inline": None,
                },
                rule_callback=lambda x, y: y,
            )

    def test_inline_empty_list(self):
        """Test method"""

        rule = InlineRule()

        parsed = rule.parse(
            rule_dict={"inline": []},
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "")

    def test_inline_list_of_str(self):
        """Test method"""

        rule = InlineRule()

        parsed = rule.parse(
            rule_dict={
                "inline": [
                    "text_1",
                    "-",
                    "text_2",
                    "-",
                    "text_3",
                ]
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text_1-text_2-text_3")

    def test_inline_list_of_func(self):
        """Test method"""

        rule = InlineRule()

        parsed = rule.parse(
            rule_dict={
                "inline": [
                    {
                        "eval": "eval_1",
                    },
                    {
                        "print": "print_1",
                    },
                    {
                        "log": "log_3",
                    },
                ],
            },
            rule_callback=TestInlineRule._rule_callback,
        )
        self.assertEqual(parsed, "eval_1print_2log_3")

    def test_inline_mix(self):
        """Test method"""

        rule = InlineRule()

        parsed = rule.parse(
            rule_dict={
                "inline": [
                    "text_1",
                    None,
                    "text_2",
                    "-",
                    "text_3",
                    "",
                    {
                        "eval": "eval_1",
                    },
                    {
                        "print": "print_1",
                    },
                    {
                        "log": "log_3",
                    },
                ],
            },
            rule_callback=TestInlineRule._rule_callback,
        )
        self.assertEqual(parsed, "text_1text_2-text_3eval_1print_2log_3")


if __name__ == "__main__":
    unittest.main()
