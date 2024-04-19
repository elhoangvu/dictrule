"""Test module"""

import unittest

from typing import (
    Any,
)

from dictrule.var_property import var_property


class VarProperty:
    """Test class"""

    def __init__(self) -> None:
        self.var_prop_a = "_prop_a"
        self.var_prop_b = "_prop_b"
        self.var_prop_c = "_prop_c"

    @var_property
    def prop_a(self):
        """Test method"""
        return self.var_prop_a

    @var_property
    def prop_b(self):
        """Test method"""
        return self.var_prop_b

    @var_property
    def prop_c(self):
        """Test method"""
        return self.var_prop_c

    @prop_a.setter
    def prop_a(self, value: Any):
        self.var_prop_a = value

    @prop_b.setter
    def prop_b(self, value: Any):
        self.var_prop_b = value

    @prop_c.setter
    def prop_c(self, value: Any):
        self.var_prop_c = value

    @prop_a.deleter
    def prop_a(self):
        del self.var_prop_a

    @prop_b.deleter
    def prop_b(self):
        del self.var_prop_b

    @prop_c.deleter
    def prop_c(self):
        del self.var_prop_c


class TestVarProperty(unittest.TestCase):
    """Test class"""

    def test_get_property(self):
        """Test method"""

        var_prop = VarProperty()
        self.assertEqual(var_prop.var_prop_a, var_prop.prop_a)
        self.assertEqual(var_prop.var_prop_b, var_prop.prop_b)
        self.assertEqual(var_prop.var_prop_c, var_prop.prop_c)

    def test_set_property(self):
        """Test method"""

        var_prop = VarProperty()
        var_prop.prop_a = "new_prop_a"
        var_prop.prop_b = "new_prop_b"
        var_prop.prop_c = "new_prop_c"
        self.assertEqual(var_prop.var_prop_a, var_prop.prop_a)
        self.assertEqual(var_prop.var_prop_b, var_prop.prop_b)
        self.assertEqual(var_prop.var_prop_c, var_prop.prop_c)

    def test_del_property(self):
        """Test method"""

        var_prop = VarProperty()
        del var_prop.prop_a
        del var_prop.prop_b
        del var_prop.prop_c
        self.assertFalse(hasattr(var_prop, "prop_a"))
        self.assertFalse(hasattr(var_prop, "prop_b"))
        self.assertFalse(hasattr(var_prop, "prop_c"))

    def test_properties(self):
        """Test method"""

        var_prop = VarProperty()
        props = var_property.properties(var_prop)
        self.assertListEqual(
            [prop.__name__ for prop in props],
            [
                getattr(var_prop.__class__, "prop_a").__name__,
                getattr(var_prop.__class__, "prop_b").__name__,
                getattr(var_prop.__class__, "prop_c").__name__,
            ],
        )

        self.assertListEqual(
            [prop.__get__(var_prop) for prop in props],
            [
                getattr(var_prop.__class__, "prop_a").__get__(var_prop),
                getattr(var_prop.__class__, "prop_b").__get__(var_prop),
                getattr(var_prop.__class__, "prop_c").__get__(var_prop),
            ],
        )


if __name__ == "__main__":
    unittest.main()
