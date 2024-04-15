"""StringifyRule test"""

from typing import (
    Dict,
    Any,
    Union,
    Optional,
)
import unittest
from dictrule.context import Context
from dictrule.built_in_rules import StringifyRule


class TestStringifyRule(unittest.TestCase):
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
            return eval_rule

        return ""

    def test_stringify(self):
        """Test method"""
        parsed = StringifyRule().parse(
            rule_dict={
                "stringify": "text",
            },
            rule_callback=TestStringifyRule._rule_callback,
        )
        self.assertEqual(parsed, '"text"')

    def test_stringify_empty(self):
        """Test method"""
        parsed = StringifyRule().parse(
            rule_dict={
                "stringify": "",
            },
            rule_callback=TestStringifyRule._rule_callback,
        )
        self.assertEqual(parsed, '""')

    def test_stringify_none(self):
        """Test method"""
        parsed = StringifyRule().parse(
            rule_dict={
                "stringify": None,
            },
            rule_callback=TestStringifyRule._rule_callback,
        )
        self.assertEqual(parsed, '""')

    def test_stringify_eval(self):
        """Test method"""
        parsed = StringifyRule().parse(
            rule_dict={
                "stringify": {
                    "eval": "123",
                },
            },
            rule_callback=TestStringifyRule._rule_callback,
        )
        self.assertEqual(parsed, '"123"')


if __name__ == "__main__":
    unittest.main()
