"""CommentRule test"""

from typing import Any
import unittest
from dictrule.context import Context
from dictrule.built_in_rules import CommentRule, EvalRule


class TestCommentRule(unittest.TestCase):
    """Test class"""

    def setUp(self) -> None:
        self._singleline_context = Context(
            [
                CommentRule.ContextCase(
                    singleline=CommentRule.ContextCase.SinglelineComment("# ")
                )
            ]
        )

        self._multiline_context = Context(
            [
                CommentRule.ContextCase(
                    multiline=CommentRule.ContextCase.MultilineComment(
                        open_comment='"""',
                        close_comment='"""',
                        prefix="# ",
                    )
                )
            ]
        )
        return super().setUp()

    def test_comment_singleline(self):
        """Test method"""

        rule = CommentRule()
        parsed = rule.parse(
            rule_dict={
                "comment": "test",
                "style": "singleline",
            },
            context=self._singleline_context,
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "# test")

    def test_comment_none(self):
        """Test method"""

        rule = CommentRule()
        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "comment": None,
                    "style": "singleline",
                },
                context=self._singleline_context,
                rule_callback=lambda x, y: y if y else "",
            )

    def test_no_comment(self):
        """Test method"""

        rule = CommentRule()
        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "style": "singleline",
                },
                context=self._singleline_context,
                rule_callback=lambda x, y: y if y else "",
            )

    def test_empty_context(self):
        """Test method"""

        rule = CommentRule()
        singleline_context = Context([])
        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "comment": "test",
                    "style": "singleline",
                },
                context=singleline_context,
                rule_callback=lambda x, y: y if y else "",
            )

    def test_comment_singleline_default(self):
        """Test method"""

        rule = CommentRule()
        parsed = rule.parse(
            rule_dict={
                "comment": "test",
            },
            context=self._singleline_context,
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "# test")

    def test_comment_singleline_empty_prefix(self):
        """Test method"""

        rule = CommentRule()
        context = Context(
            [
                CommentRule.ContextCase(
                    singleline=CommentRule.ContextCase.SinglelineComment(
                        prefix="",
                    )
                )
            ]
        )

        parsed = rule.parse(
            rule_dict={
                "comment": "test",
                "style": "singleline",
            },
            context=context,
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "test")

    def test_comment_singleline_none_context(self):
        """Test method"""

        rule = CommentRule()
        context = Context([])
        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "comment": "test",
                },
                context=context,
                rule_callback=lambda x, y: y if y else "",
            )

    def test_comment_singleline_list(self):
        """Test method"""

        rule = CommentRule()
        parsed = rule.parse(
            rule_dict={
                "style": "singleline",
                "comment": [
                    "text_1",
                    "text_2",
                    "text_3",
                ],
            },
            context=self._singleline_context,
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "# text_1\n# text_2\n# text_3")

    def test_comment_multiline(self):
        """Test method"""

        rule = CommentRule()
        parsed = rule.parse(
            rule_dict={
                "comment": "test",
                "style": "multiline",
            },
            context=self._multiline_context,
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, '"""\n# test\n"""')

    def test_comment_multiline_none_context(self):
        """Test method"""

        rule = CommentRule()
        context = Context([])

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "comment": "test",
                    "style": "multiline",
                },
                context=context,
                rule_callback=lambda x, y: y if y else "",
            )

    def test_comment_multiline_empty_config(self):
        """Test method"""

        rule = CommentRule()
        context = Context(
            [
                CommentRule.ContextCase(
                    multiline=CommentRule.ContextCase.MultilineComment(
                        prefix="",
                        open_comment="",
                        close_comment="",
                    )
                )
            ]
        )

        parsed = rule.parse(
            rule_dict={
                "comment": "test",
                "style": "multiline",
            },
            context=context,
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, "test")

    def test_comment_multiline_list(self):
        """Test method"""

        rule = CommentRule()
        parsed = rule.parse(
            rule_dict={
                "style": "multiline",
                "comment": [
                    "text_1",
                    "text_2",
                    "text_3",
                ],
            },
            context=self._multiline_context,
            rule_callback=lambda x, y: y if y else "",
        )
        self.assertEqual(parsed, '"""\n# text_1\n# text_2\n# text_3\n"""')

    def test_comment_single_func(self):
        """Test method"""

        class DummyEvaluator(EvalRule.Evaluable):
            """Test class"""

            @property
            def name(self) -> str:
                """Test method"""
                return "test"

            def run(self, cmd: str) -> Any:
                """Test method"""
                _ = cmd
                return "dummy"

        rule = CommentRule()

        singleline_context = Context(
            [
                CommentRule.ContextCase(
                    singleline=CommentRule.ContextCase.SinglelineComment("# ")
                ),
                EvalRule.ContextCase(
                    evaluators=[
                        DummyEvaluator(),
                    ],
                ),
            ]
        )

        parsed = rule.parse(
            rule_dict={
                "style": "singleline",
                "comment": {
                    "eval": "test",
                },
            },
            context=singleline_context,
            rule_callback=lambda x, y: x.get(EvalRule.CONTEXT_NAME).eval(
                list(y.values())[0]
            ),
        )
        self.assertEqual(parsed, "# dummy")


if __name__ == "__main__":
    unittest.main()
