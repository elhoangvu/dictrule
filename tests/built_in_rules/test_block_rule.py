"""BlockRule test"""

from typing import (
    Optional,
    Union,
    Dict,
    Any,
)

import unittest
from dictrule.context import Context
from dictrule.built_in_rules import BlockRule


class TestBlockRule(unittest.TestCase):
    """Test class"""

    def test_parse(self):
        """Test method"""

        rule = BlockRule()
        parsed = rule.parse(
            rule_dict={
                "block": [
                    "text_1",
                    "text_2",
                    "text_3",
                ]
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text_1\ntext_2\ntext_3")

    def test_parse_none(self):
        """Test method"""

        rule = BlockRule()
        parsed = rule.parse(
            rule_dict={
                "block": [
                    None,
                    None,
                    None,
                ]
            },
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "\n\n")

    def test_parse_empty(self):
        """Test method"""

        rule = BlockRule()
        parsed = rule.parse(
            rule_dict={"block": []},
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "")

    def test_parse_none_block(self):
        """Test method"""

        rule = BlockRule()
        with self.assertRaises(Exception):
            rule.parse(
                rule_dict={
                    "block": None,
                },
                rule_callback=lambda x, y: y if y else "",
            )

    def test_parse_no_block(self):
        """Test method"""

        rule = BlockRule()
        with self.assertRaises(Exception):
            rule.parse(
                rule_dict={},
                rule_callback=lambda x, y: y if y else "",
            )

    def test_parse_func(self):
        """Test method"""

        rule = BlockRule()

        def _rule_callback(
            context: Optional[Context],
            rule: Dict[str, Any],
        ) -> str:
            _ = context
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

        parsed = rule.parse(
            rule_dict={
                "block": [
                    {
                        "eval": "echo_1",
                    },
                    {
                        "print": "echo_2",
                    },
                    {
                        "log": "echo_e",
                    },
                ]
            },
            rule_callback=_rule_callback,
        )
        self.assertEqual(parsed, "eval_1\nprint_2\nlog_3")

    def test_parse_mix(self):
        """Test method"""

        rule = BlockRule()

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

        parsed = rule.parse(
            rule_dict={
                "block": [
                    {
                        "eval": "echo_1",
                    },
                    {
                        "print": "echo_2",
                    },
                    {
                        "log": "echo_e",
                    },
                    "text_4",
                    "",
                    "text_5",
                    None,
                    "text_6",
                    None,
                ]
            },
            rule_callback=_rule_callback,
        )
        self.assertEqual(parsed, "eval_1\nprint_2\nlog_3\ntext_4\n\ntext_5\n\ntext_6\n")


if __name__ == "__main__":
    unittest.main()
