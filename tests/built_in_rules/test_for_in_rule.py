"""ForInRule test"""

from typing import Any, Dict, Optional
from dictrule.context import Context
from dictrule.built_in_rules import ForInRule, EvalRule
import unittest


class TestForInRule(unittest.TestCase):
    """Test class"""

    class Line:
        """Test class"""

        def __init__(
            self,
            text: str,
        ):
            self.text = text
            self.len = len(text)

    class LineEvaluator(EvalRule.Evaluable):
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
                TestForInRule.Line("text_1"),
                TestForInRule.Line("text_text_2"),
                TestForInRule.Line("text_text_text_3"),
            ]

    class NestObjEvaluator(EvalRule.Evaluable):
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

        class Obj:
            """Test class"""

            def __init__(
                self,
                obj: Any,
            ):
                self.obj = obj

        def run(self, cmd: str) -> Any:
            """Test method"""
            _ = cmd
            return [
                TestForInRule.NestObjEvaluator.Obj(
                    TestForInRule.NestObjEvaluator.Obj("text")
                ),
                TestForInRule.NestObjEvaluator.Obj(
                    TestForInRule.NestObjEvaluator.Obj("text_1")
                ),
            ]

    class LineEvaluatorNotIterable(EvalRule.Evaluable):
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
            return 1

    class LineEvaluatorStr(EvalRule.Evaluable):
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
            return "xyz"

    @staticmethod
    def __rule_callback(
        context: Optional[Context],
        rule: str | Dict[str, Any],
    ) -> str:
        if not rule:
            return ""

        if isinstance(rule, str):
            return rule

        if "eval" in rule:
            return EvalRule().parse(
                rule_dict=rule,
                rule_callback=TestForInRule.__rule_callback,
                context=context,
            )

        return ""

    def test_for_in(self):
        """Test method"""

        rule = ForInRule()

        parsed = rule.parse(
            rule_dict={
                "for": "line",
                "in": "lines",
                "block": [
                    "text",
                    {
                        "eval": "line.index",
                    },
                    {
                        "eval": "line.text",
                    },
                    {
                        "eval": "line.len",
                    },
                ],
            },
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators=[TestForInRule.LineEvaluator("lines")],
                    )
                ]
            ),
            rule_callback=TestForInRule.__rule_callback,
        )

        self.assertEqual(
            parsed,
            "text\n0\ntext_1\n6\ntext\n1\ntext_text_2\n11\ntext\n2\ntext_text_text_3\n16",
        )

    def test_for_in_empty_block(self):
        """Test method"""

        rule = ForInRule()

        parsed = rule.parse(
            rule_dict={"for": "line", "in": "lines", "block": []},
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators=[TestForInRule.LineEvaluator("lines")],
                    )
                ]
            ),
            rule_callback=TestForInRule.__rule_callback,
        )

        self.assertEqual(parsed, "\n\n")

    def test_for_in_none_for(self):
        """Test method"""

        rule = ForInRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={"for": None, "in": "lines", "block": []},
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[TestForInRule.LineEvaluator("lines")],
                        )
                    ]
                ),
                rule_callback=TestForInRule.__rule_callback,
            )

    def test_for_in_none_in(self):
        """Test method"""

        rule = ForInRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={"for": "line", "in": None, "block": []},
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[TestForInRule.LineEvaluator("lines")],
                        )
                    ]
                ),
                rule_callback=TestForInRule.__rule_callback,
            )

    def test_for_in_none_block(self):
        """Test method"""

        rule = ForInRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "for": "line",
                    "in": "lines",
                    "block": None,
                },
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[TestForInRule.LineEvaluator("lines")],
                        )
                    ]
                ),
                rule_callback=TestForInRule.__rule_callback,
            )

    def test_for_in_none_block_2(self):
        """Test method"""

        rule = ForInRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "for": "line",
                    "in": "lines",
                    "block": [],
                },
                context=Context(
                    [
                        EvalRule.ContextCase(
                            evaluators=[
                                TestForInRule.LineEvaluatorNotIterable("lines")
                            ],
                        )
                    ]
                ),
                rule_callback=TestForInRule.__rule_callback,
            )

    def test_for_in_str(self):
        """Test method"""

        rule = ForInRule()

        parsed = rule.parse(
            rule_dict={
                "for": "line",
                "in": "lines",
                "block": [
                    {
                        "eval": "line",
                    },
                ],
            },
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators=[TestForInRule.LineEvaluatorStr("lines")],
                    )
                ]
            ),
            rule_callback=TestForInRule.__rule_callback,
        )

        self.assertEqual(parsed, "x\ny\nz")

    def test_for_in_nestes_call(self):
        """Test method"""

        rule = ForInRule()

        parsed = rule.parse(
            rule_dict={
                "for": "line",
                "in": "lines",
                "block": [
                    {
                        "eval": "line.obj.obj",
                    },
                ],
            },
            context=Context(
                [
                    EvalRule.ContextCase(
                        evaluators=[TestForInRule.NestObjEvaluator("lines")],
                    )
                ]
            ),
            rule_callback=TestForInRule.__rule_callback,
        )

        self.assertEqual(parsed, "text\ntext_1")


if __name__ == "__main__":
    unittest.main()
