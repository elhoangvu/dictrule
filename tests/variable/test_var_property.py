"""Test module"""

import unittest

from typing import (
    Any,
)

from dictrule.eo_property import eo_property


class ObjProperty:
    """Test class"""

    def __init__(self) -> None:
        self.obj_prop_a = "_prop_a"
        self.obj_prop_b = "_prop_b"
        self.obj_prop_c = "_prop_c"

    @eo_property
    def prop_a(self):
        """Test method"""
        return self.obj_prop_a

    @eo_property
    def prop_b(self):
        """Test method"""
        return self.obj_prop_b

    @eo_property
    def prop_c(self):
        """Test method"""
        return self.obj_prop_c

    @prop_a.setter
    def prop_a(self, value: Any):
        self.obj_prop_a = value

    @prop_b.setter
    def prop_b(self, value: Any):
        self.obj_prop_b = value

    @prop_c.setter
    def prop_c(self, value: Any):
        self.obj_prop_c = value

    @prop_a.deleter
    def prop_a(self):
        del self.obj_prop_a

    @prop_b.deleter
    def prop_b(self):
        del self.obj_prop_b

    @prop_c.deleter
    def prop_c(self):
        del self.obj_prop_c


class TestVarProperty(unittest.TestCase):
    """Test class"""

    def test_get_property(self):
        """Test method"""

        obj_prop = ObjProperty()
        self.assertEqual(obj_prop.obj_prop_a, obj_prop.prop_a)
        self.assertEqual(obj_prop.obj_prop_b, obj_prop.prop_b)
        self.assertEqual(obj_prop.obj_prop_c, obj_prop.prop_c)

    def test_set_property(self):
        """Test method"""

        obj_prop = ObjProperty()
        obj_prop.prop_a = "new_prop_a"
        obj_prop.prop_b = "new_prop_b"
        obj_prop.prop_c = "new_prop_c"
        self.assertEqual(obj_prop.obj_prop_a, obj_prop.prop_a)
        self.assertEqual(obj_prop.obj_prop_b, obj_prop.prop_b)
        self.assertEqual(obj_prop.obj_prop_c, obj_prop.prop_c)

    def test_del_property(self):
        """Test method"""

        obj_prop = ObjProperty()
        del obj_prop.prop_a
        del obj_prop.prop_b
        del obj_prop.prop_c
        self.assertFalse(hasattr(obj_prop, "prop_a"))
        self.assertFalse(hasattr(obj_prop, "prop_b"))
        self.assertFalse(hasattr(obj_prop, "prop_c"))

    def test_properties(self):
        """Test method"""

        obj_prop = ObjProperty()
        props = eo_property.properties(obj_prop)
        self.assertListEqual(
            [prop.__name__ for prop in props],
            [
                getattr(obj_prop.__class__, "prop_a").__name__,
                getattr(obj_prop.__class__, "prop_b").__name__,
                getattr(obj_prop.__class__, "prop_c").__name__,
            ],
        )

        self.assertListEqual(
            [prop.__get__(obj_prop) for prop in props],
            [
                getattr(obj_prop.__class__, "prop_a").__get__(obj_prop),
                getattr(obj_prop.__class__, "prop_b").__get__(obj_prop),
                getattr(obj_prop.__class__, "prop_c").__get__(obj_prop),
            ],
        )


if __name__ == "__main__":
    unittest.main()
