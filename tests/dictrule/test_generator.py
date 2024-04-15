"""DictRule test"""

from typing import Any
from pathlib import Path
import unittest
import yaml
from dictrule.context import Context
from dictrule.generator import Generator
from dictrule.built_in_rules import CommentRule, EvalRule


class TestGenerator(unittest.TestCase):
    """Test class"""

    class TestEvaluator(EvalRule.Evaluable):
        """Test class"""

        EVALS = {
            "content-123": "Content one two three",
            "content": "CoNteNt",
            "ends": [
                "text-1",
                "text-2",
                "text-3",
            ],
        }

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

            return TestGenerator.TestEvaluator.EVALS.get(cmd)

    class TestGenEvaluator(EvalRule.Evaluable):
        """Test class"""

        EVALS = {
            "gen.header": "THIS IS THE GENERATED EXAMPLE CODE",
            "gen.id": 3101,
            "gen.title": "Sampler for getting sample contents",
            "gen.date": "01-01-2024",
            "gen.author": "Zooxy Le",
            "gen.contents": ["Train", "Flight", "Ship"],
        }

        @property
        def name(self) -> str:
            return "gen."

        @property
        def prefix_matching(self) -> bool:
            return True

        def run(self, cmd: str) -> Any:
            """Test method"""

            return TestGenerator.TestGenEvaluator.EVALS.get(cmd)

    def test_empty_gen_rules(self):
        """Test method"""

        gen_rules = []
        generator = Generator(gen_rules=gen_rules)
        self.assertListEqual(generator.gen_rules, [])

    def test_gen_rules(self):
        """Test method"""

        gen_rules = [
            "123",
            "text",
        ]
        generator = Generator(gen_rules=gen_rules)
        self.assertListEqual(generator.gen_rules, gen_rules)

    def test_empty_parse_rules(self):
        """Test method"""

        generator = Generator(
            gen_rules=[],
            parse_rules=[],
        )
        self.assertListEqual(generator.parse_rules, [])

    def test_std_parse_rules(self):
        """Test method"""

        generator = Generator(
            gen_rules=[],
            parse_rules=Generator.STD_RULES,
        )
        self.assertListEqual(generator.parse_rules, Generator.STD_RULES)

    def test_add_parse_rule(self):
        """Test method"""

        generator = Generator(
            gen_rules=[],
            parse_rules=[],
        )
        rule = TestGenerator.TestEvaluator("123")
        generator.add_parse_rule(rule)
        self.assertListEqual(generator.parse_rules, [rule])

    def test_add_parse_rules(self):
        """Test method"""

        generator = Generator(
            gen_rules=[],
            parse_rules=[],
        )
        parse_rules = [
            TestGenerator.TestEvaluator("123"),
            TestGenerator.TestEvaluator("456"),
        ]
        generator.add_parse_rules(parse_rules)
        self.assertListEqual(generator.parse_rules, parse_rules)

    def test_generate(self):
        """Test method"""

        generator = Generator(
            gen_rules=[
                "header",
                {
                    "block": [
                        "subtitle_1",
                        "subtitle_2",
                    ],
                },
                {
                    "comment": "desc",
                },
                {
                    "eval": "content",
                },
                {
                    "format_uppercase": "code_1",
                },
                {
                    "format_lowercase": "CODE_2",
                },
                {
                    "format_upper_head": "myCode_3",
                },
                {
                    "indent_0": "class MyClass:",
                },
                {
                    "indent_1": "def func(self):",
                },
                {
                    "indent_2": "return 0",
                },
                {
                    "inline": ["py", "-", "code", "-", "example"],
                },
                {
                    "join": ".",
                    "block": [
                        "text_1",
                        "text_2",
                        "text_3",
                    ],
                },
                {"join": ".", "eval": "ends"},
            ],
        )

        context = Context(
            [
                EvalRule.ContextCase(
                    evaluators=[
                        TestGenerator.TestEvaluator("content"),
                        TestGenerator.TestEvaluator("ends"),
                    ],
                ),
                CommentRule.ContextCase(
                    singleline=CommentRule.ContextCase.SinglelineComment("# ")
                ),
            ]
        )

        generated = generator.generate(context)
        self.assertEqual(
            generated,
            f"""header
subtitle_1
subtitle_2
# desc
{TestGenerator.TestEvaluator.EVALS['content']}
CODE_1
code_2
MyCode_3
class MyClass:
  def func(self):
    return 0
py-code-example
text_1.text_2.text_3
{'.'.join(TestGenerator.TestEvaluator.EVALS['ends'])}""",
        )

    def test_generate_from_file(self):
        """Test method"""

        file_path = Path(__file__).parent / "test_dictrule.yml"
        file = open(
            file=file_path,
            mode="r",
            encoding="utf-8",
        )
        rules = yaml.safe_load(file)
        generator = Generator(
            gen_rules=rules,
        )

        context = Context(
            [
                EvalRule.ContextCase(
                    evaluators=[TestGenerator.TestGenEvaluator()],
                ),
                CommentRule.ContextCase(
                    singleline=CommentRule.ContextCase.SinglelineComment("# ")
                ),
            ]
        )

        generated = generator.generate(context)
        self.assertEqual(
            generated,
            '''"""
THIS IS THE GENERATED EXAMPLE CODE
"""

# 3101. Sampler for getting sample contents
# Creation date: 01-01-2024
# Author: Zooxy Le

class Sample:
  def contents(self) -> List[str]:
    return [
      "0",
      "Train",
      "1",
      "Flight",
      "2",
      "Ship",
    ]''',
        )


if __name__ == "__main__":
    unittest.main()
