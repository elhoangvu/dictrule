"""JoinEvalRule test"""

from typing import Any
from dictrule.context import Context
from dictrule.built_in_rules import JoinEvalRule, EvalRule
import unittest


class TestJoinEvalRule(unittest.TestCase):
    """Test class"""

    class IterableEvaluator(EvalRule.Evaluable):
        """Test class"""

        def __init__(
            self,
            name: str,
        ):
            self.__name = name

        @property
        def name(self) -> str:
            """Test method"""
            return self.__name

        def run(self, cmd: str) -> Any:
            """Test method"""
            _ = cmd
            return [
                "text_1",
                "text_2",
                "text_3",
            ]

    class NonIterableEvaluator(EvalRule.Evaluable):
        """Test class"""

        def __init__(
            self,
            name: str,
        ):
            self.__name = name

        @property
        def name(self) -> str:
            """Test method"""
            return self.__name

        def run(self, cmd: str) -> Any:
            """Test method"""
            _ = cmd
            return 123

    def test_join_not_evaluable(self):
        """Test method"""

        rule = JoinEvalRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "join": ",",
                    "eval": "test",
                },
                context=Context([EvalRule.ContextCase([])]),
                rule_callback=lambda x, y: y,
            )

    def test_join_not_evaluable_2(self):
        """Test method"""

        rule = JoinEvalRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "join": ",",
                    "eval": "test",
                },
                context=Context(
                    [
                        EvalRule.ContextCase(
                            [TestJoinEvalRule.NonIterableEvaluator("test")]
                        )
                    ]
                ),
                rule_callback=lambda x, y: y,
            )

    def test_join_evaluable(self):
        """Test method"""

        rule = JoinEvalRule()

        parsed = rule.parse(
            rule_dict={
                "join": ",",
                "eval": "test",
            },
            context=Context(
                [EvalRule.ContextCase([TestJoinEvalRule.IterableEvaluator("test")])]
            ),
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text_1,text_2,text_3")

    def test_join_none_eval(self):
        """Test method"""

        rule = JoinEvalRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "join": ",",
                    "eval": None,
                },
                context=Context(
                    [EvalRule.ContextCase([TestJoinEvalRule.IterableEvaluator("test")])]
                ),
                rule_callback=lambda x, y: y,
            )

    def test_join_empty_separator(self):
        """Test method"""

        rule = JoinEvalRule()

        parsed = rule.parse(
            rule_dict={
                "join": "",
                "eval": "test",
            },
            context=Context(
                [EvalRule.ContextCase([TestJoinEvalRule.IterableEvaluator("test")])]
            ),
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text_1text_2text_3")

    def test_join_none_separator(self):
        """Test method"""

        rule = JoinEvalRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "join": None,
                    "eval": "test",
                },
                context=Context(
                    [EvalRule.ContextCase([TestJoinEvalRule.IterableEvaluator("test")])]
                ),
                rule_callback=lambda x, y: y,
            )


if __name__ == "__main__":
    unittest.main()
