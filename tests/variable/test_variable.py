"""Test module"""

import unittest

from typing import (
    Any,
    Set,
    List,
    Dict,
)

from dictrule.eo_property import eo_property
from dictrule.eval_object import EvalObject


class ObjProperty:
    """Test class"""

    def __init__(self) -> None:
        self.obj_prop_a = "_prop_a"
        self.obj_prop_b = "_prop_b"
        self.obj_prop_c = "_prop_c"
        self.obj_prop_d = "_prop_d"

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

    @property
    def prop_d(self):
        """Test method"""
        return self.obj_prop_d


class ComplexObject:
    """Test class"""

    def __init__(self) -> None:
        self.obj_prop_a = [
            ObjProperty(),
            ObjProperty(),
            ObjProperty(),
        ]

        self.obj_prop_b = set(self.obj_prop_a)

        self.obj_prop_c = {
            "1": self.obj_prop_a[0],
            "2": self.obj_prop_a[1],
            "3": self.obj_prop_a[2],
        }

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


class TestObject(unittest.TestCase):
    """Test class"""

    def test_object(self):
        """Test method"""

        obj_prop = ObjProperty()
        obj = EvalObject.from_eo_property_object(obj_prop)
        self.assertEqual(getattr(obj, "prop_a"), obj_prop.prop_a)
        self.assertEqual(getattr(obj, "prop_b"), obj_prop.prop_b)
        self.assertEqual(getattr(obj, "prop_c"), obj_prop.prop_c)
        self.assertFalse(hasattr(obj, "prop_d"))

    def test_list_of_objects(self):
        """Test method"""

        obj_prop_list = [
            ObjProperty(),
            ObjProperty(),
            ObjProperty(),
        ]
        obj_list: List[Any] = EvalObject.from_eo_property_object(obj_prop_list)
        self.assertEqual(len(obj_prop_list), len(obj_list))
        self.assertTrue(isinstance(obj_list, list))
        length = len(obj_prop_list)
        for i in range(length):
            self.assertEqual(getattr(obj_list[i], "prop_a"), obj_prop_list[i].prop_a)
            self.assertEqual(getattr(obj_list[i], "prop_b"), obj_prop_list[i].prop_b)
            self.assertEqual(getattr(obj_list[i], "prop_c"), obj_prop_list[i].prop_c)
            self.assertFalse(hasattr(obj_list[i], "prop_d"))

    def test_set_of_objects(self):
        """Test method"""

        obj_prop_list = [
            ObjProperty(),
            ObjProperty(),
            ObjProperty(),
        ]
        obj_prop_set = set(obj_prop_list)
        obj_set: Set[Any] = EvalObject.from_eo_property_object(obj_prop_set)
        self.assertEqual(len(obj_prop_set), len(obj_set))
        self.assertTrue(isinstance(obj_set, set))

        index = 0
        for obj in obj_set:
            self.assertEqual(getattr(obj, "prop_a"), obj_prop_list[index].prop_a)
            self.assertEqual(getattr(obj, "prop_b"), obj_prop_list[index].prop_b)
            self.assertEqual(getattr(obj, "prop_c"), obj_prop_list[index].prop_c)
            self.assertFalse(hasattr(obj, "prop_d"))
            index += 1

    def test_dict_of_objects(self):
        """Test method"""

        obj_prop_dict = {
            "1": ObjProperty(),
            "2": ObjProperty(),
            "3": ObjProperty(),
        }
        obj_dict: Dict[Any, Any] = EvalObject.from_eo_property_object(obj_prop_dict)
        self.assertEqual(len(obj_prop_dict), len(obj_dict))
        self.assertTrue(isinstance(obj_dict, dict))

        for key, obj in obj_dict.items():
            self.assertEqual(getattr(obj, "prop_a"), obj_prop_dict[key].prop_a)
            self.assertEqual(getattr(obj, "prop_b"), obj_prop_dict[key].prop_b)
            self.assertEqual(getattr(obj, "prop_c"), obj_prop_dict[key].prop_c)
            self.assertFalse(hasattr(obj, "prop_d"))

    def test_add_object(self):
        """Test method"""

        obj_prop = ObjProperty()
        obj: EvalObject = EvalObject.from_eo_property_object(obj_prop)
        self.assertFalse(hasattr(obj, "prop_d"))
        obj.add_object(0, "prop_d")
        self.assertTrue(hasattr(obj, "prop_d"))

    def test_complex_objects(self):
        """Test method"""

        complex_obj = ComplexObject()
        obj: ComplexObject = EvalObject.from_eo_property_object(complex_obj)
        self.assertTrue(isinstance(obj.prop_a, list))
        self.assertTrue(isinstance(obj.prop_b, set))
        self.assertTrue(isinstance(obj.prop_c, dict))

        length = len(obj.prop_a)
        for i in range(length):
            self.assertEqual(getattr(obj.prop_a[i], "prop_a"), obj.prop_a[i].prop_a)
            self.assertEqual(getattr(obj.prop_a[i], "prop_b"), obj.prop_a[i].prop_b)
            self.assertEqual(getattr(obj.prop_a[i], "prop_c"), obj.prop_a[i].prop_c)

        for obj_b in obj.prop_b:
            self.assertEqual(getattr(obj_b, "prop_a"), obj.prop_a[0].prop_a)
            self.assertEqual(getattr(obj_b, "prop_b"), obj.prop_a[0].prop_b)
            self.assertEqual(getattr(obj_b, "prop_c"), obj.prop_a[0].prop_c)

        for key, obj_c in obj.prop_c.items():
            self.assertEqual(getattr(obj_c, "prop_a"), obj.prop_c[key].prop_a)
            self.assertEqual(getattr(obj_c, "prop_b"), obj.prop_c[key].prop_b)
            self.assertEqual(getattr(obj_c, "prop_c"), obj.prop_c[key].prop_c)


if __name__ == "__main__":
    unittest.main()
