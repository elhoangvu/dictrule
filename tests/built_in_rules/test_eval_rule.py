"""EvalRule test"""

import unittest
from typing import Any
from dictrule.context import Context
from dictrule.built_in_rules import EvalRule


class TestEvalRule(unittest.TestCase):
    """Test class"""

    class DummyEvaluator(EvalRule.Evaluable):
        """Test class"""

        def __init__(
            self,
            name: str,
        ):
            self._name = name

        @property
        def name(self) -> str:
            """Test method"""
            return self._name

        def run(self, cmd: str) -> Any:
            """Test method"""
            _ = cmd
            return "dummy"

    class LoremEvaluator(EvalRule.Evaluable):
        """Test class"""

        def __init__(
            self,
            name: str,
        ):
            self._name = name

        @property
        def name(self) -> str:
            """Test method"""
            return self._name

        def run(self, cmd: str) -> Any:
            """Test method"""
            _ = cmd
            return "lorem"

    def test_eval_empty(self):
        """Test method"""

        rule = EvalRule()

        parsed = rule.parse(
            rule_dict={"eval": ""},
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators=[
                            TestEvalRule.DummyEvaluator(""),
                        ],
                    )
                ]
            ),
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "dummy")

    def test_eval_no_context(self):
        """Test method"""

        rule = EvalRule()

        with self.assertRaises(Exception):
            rule.parse(
                rule_dict={
                    "eval": "test",
                },
                rule_callback=lambda x, y: y if y else "",
            )

    def test_eval_none_eval(self):
        """Test method"""

        rule = EvalRule()

        with self.assertRaises(Exception):
            rule.parse(
                rule_dict={
                    "eval": None,
                },
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[
                                TestEvalRule.DummyEvaluator(""),
                            ],
                        )
                    ]
                ),
                rule_callback=lambda x, y: y if y else "",
            )

    def test_eval_no_eval(self):
        """Test method"""

        rule = EvalRule()

        with self.assertRaises(Exception):
            rule.parse(
                rule_dict={},
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[],
                        )
                    ]
                ),
                rule_callback=lambda x, y: y if y else "",
            )

    def test_eval_no_context_2(self):
        """Test method"""

        rule = EvalRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={"eval": "test"},
                context=Context([]),
                rule_callback=lambda x, y: y if y else "",
            )

    def test_eval(self):
        """Test method"""

        rule = EvalRule()

        parsed = rule.parse(
            rule_dict={
                "eval": "test",
            },
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators=[
                            TestEvalRule.LoremEvaluator("test"),
                        ]
                    )
                ]
            ),
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "lorem")

    def test_eval_fallback(self):
        """Test method"""

        rule = EvalRule()

        parsed = rule.parse(
            rule_dict={
                "eval": "test",
            },
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators={},
                        fallback=TestEvalRule.LoremEvaluator("dummy"),
                    )
                ]
            ),
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "lorem")

    def test_eval_no_fallback(self):
        """Test method"""

        rule = EvalRule()

        parsed = rule.parse(
            rule_dict={
                "eval": "test",
            },
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators=[
                            TestEvalRule.DummyEvaluator("test"),
                        ],
                        fallback=TestEvalRule.LoremEvaluator("dummy"),
                    )
                ]
            ),
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "dummy")

    def test_eval_fallback_none_evaluable(self):
        """Test method"""

        rule = EvalRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "eval": None,
                },
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[],
                            fallback=TestEvalRule.LoremEvaluator(""),
                        )
                    ]
                ),
                rule_callback=lambda x, y: y if y else "",
            )

    def test_eval_no_match(self):
        """Test method"""

        rule = EvalRule()
        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "eval": "test",
                },
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[
                                TestEvalRule.LoremEvaluator("test_2"),
                            ],
                        )
                    ]
                ),
                rule_callback=lambda x, y: y if y else "",
            )


if __name__ == "__main__":
    unittest.main()
