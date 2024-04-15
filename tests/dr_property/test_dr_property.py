"""dr_property test"""

import unittest

from typing import Dict, Any, List, Callable
from dictrule.dr_property import dr_property


class MyClass:
    """Test class"""

    @dr_property()
    def _for(self, props: Dict[str, Any]):
        pass

    @dr_property()
    def _in(self, props: Dict[str, Any]):
        pass

    @dr_property()
    def _block(self, props: Dict[str, Any]):
        pass

    def parse(self, props: Dict[str, Any]) -> List[str]:
        """Test method"""

        return [
            self._for(props),
            self._in(props),
            self._block(props),
        ]


class MyPrefixClass:
    """Test class"""

    @dr_property(prefix_matching=True)
    def _for(self, props: Dict[str, Any]):
        pass

    @dr_property(prefix_matching=True)
    def _in(self, props: Dict[str, Any]):
        pass

    @dr_property(prefix_matching=True)
    def _block(self, props: Dict[str, Any]):
        pass

    def parse(self, props: Dict[str, Any]) -> List[str]:
        """Test method"""

        return [
            self._for(props),
            self._in(props),
            self._block(props),
        ]


class OptionalPrefixClass:
    """Test class"""

    @dr_property(prefix_matching=True)
    def _for(self, props: Dict[str, Any]):
        pass

    @dr_property(prefix_matching=True, optional=True)
    def _in(self, props: Dict[str, Any]):
        pass

    @dr_property(optional=True)
    def _block(self, props: Dict[str, Any]):
        pass

    def parse(self, props: Dict[str, Any]) -> List[str]:
        """Test method"""

        return [
            self._for(props),
            self._in(props),
            self._block(props),
        ]


class TestDRProperty(unittest.TestCase):
    """Test class"""

    def test_dr_property_call(self):
        """Test method"""

        props = {
            "for": "for_text",
            "in": "in_text",
            "block": "block_text",
        }

        parsed = MyClass().parse(props)
        self.assertListEqual(
            parsed,
            [
                ("for", "for_text"),
                ("in", "in_text"),
                ("block", "block_text"),
            ],
        )

    def test_dr_property_prefix(self):
        """Test method"""

        props = {
            "for_1": "for_text",
            "in_2": "in_text",
            "block_3": "block_text",
        }

        self.assertListEqual(
            MyPrefixClass().parse(props),
            [
                ("for_1", "for_text"),
                ("in_2", "in_text"),
                ("block_3", "block_text"),
            ],
        )

    def test_properties(self):
        """Test method"""

        instace = MyClass()
        properties = dr_property.properties(instace)
        self.assertListEqual(
            sorted([prop.__name__ for prop in properties]),
            sorted(
                [
                    "_for",
                    "_in",
                    "_block",
                ]
            ),
        )

    def test_str_properties(self):
        """Test method"""

        instace = MyClass()
        properties = dr_property.str_properties(instace)
        self.assertListEqual(
            sorted(properties),
            sorted(
                [
                    "for",
                    "in",
                    "block",
                ]
            ),
        )

    def test_properties_are_property(self):
        """Test method"""

        instace = MyClass()
        properties = dr_property.properties(instace)
        for prop in properties:
            self.assertIsInstance(prop, Callable)

    def test_properties_optional(self):
        """Test method"""

        my_class = OptionalPrefixClass()
        properties = dr_property.properties(my_class, optional=False)
        self.assertListEqual(
            sorted([prop.__name__ for prop in properties]), sorted(["_for"])
        )


if __name__ == "__main__":
    unittest.main()
