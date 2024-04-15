"""JoinBlockRule test"""

from typing import (
    Optional,
    Union,
    Dict,
    Any,
)
import unittest
from dictrule.context import Context
from dictrule.built_in_rules import JoinBlockRule


class TestJoinBlockRule(unittest.TestCase):
    """Test method"""

    @staticmethod
    def __rule_callback(
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

    def test_join(self):
        """Test method"""

        rule = JoinBlockRule()

        parsed = rule.parse(
            rule_dict={
                "join": ",",
                "block": [
                    "text_1",
                    "text_2",
                    "text_3",
                ],
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text_1,text_2,text_3")

    def test_join_empty_block(self):
        """Test method"""

        rule = JoinBlockRule()

        parsed = rule.parse(
            rule_dict={"join": ",", "block": []},
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "")

    def test_join_empty_separator(self):
        """Test method"""

        rule = JoinBlockRule()

        parsed = rule.parse(
            rule_dict={
                "join": "",
                "block": [
                    "text_1",
                    "text_2",
                    "text_3",
                ],
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text_1text_2text_3")

    def test_join_none_separator(self):
        """Test method"""

        rule = JoinBlockRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "join": None,
                    "block": [
                        "text_1",
                        "text_2",
                        "text_3",
                    ],
                },
                rule_callback=lambda x, y: y,
            )

    def test_join_none_block(self):
        """Test method"""

        rule = JoinBlockRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "join": "",
                    "block": None,
                },
                rule_callback=lambda x, y: y,
            )

    def test_join_mix_block(self):
        """Test method"""

        rule = JoinBlockRule()

        parsed = rule.parse(
            rule_dict={
                "join": ".",
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
                ],
            },
            rule_callback=TestJoinBlockRule.__rule_callback,
        )
        self.assertEqual(parsed, "eval_1.print_2.log_3.text_4..text_5..text_6.")


if __name__ == "__main__":
    unittest.main()
