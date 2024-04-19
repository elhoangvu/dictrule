"""Test module"""

import unittest
from dictrule.context import Context
from dictrule.exceptions import (
    InvalidValueException,
)


class DummyContext(Context):
    """Test class"""


class DummyContextCase(Context.Case):
    """Test class"""

    def __init__(
        self,
        name: str,
    ):
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class TestContext(unittest.TestCase):
    """Test class"""

    def test_context(self):
        """Test method"""

        cases = [
            DummyContextCase("name_1"),
            DummyContextCase("name_2"),
            DummyContextCase("name_3"),
        ]
        context = DummyContext(cases)
        self.assertListEqual(context.cases, cases)
        self.assertDictEqual(context.case_map, {case.name: case for case in cases})
        for case in cases:
            self.assertEqual(case, context.get(case.name))

    def test_duplicate_case(self):
        """Test method"""

        with self.assertRaises(InvalidValueException):
            _ = DummyContext([DummyContextCase("dummy"), DummyContextCase("dummy")])


if __name__ == "__main__":
    unittest.main()
