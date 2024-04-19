"""Test module"""

import unittest

from typing import (
    Any,
    Set,
    List,
    Dict,
)

from dictrule.var_property import var_property
from dictrule.variable import Variable


class VarProperty:
    """Test class"""

    def __init__(self) -> None:
        self.var_prop_a = "_prop_a"
        self.var_prop_b = "_prop_b"
        self.var_prop_c = "_prop_c"
        self.var_prop_d = "_prop_d"

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

    @property
    def prop_d(self):
        """Test method"""
        return self.var_prop_d


class ComplexVariable:
    """Test class"""

    def __init__(self) -> None:
        self.var_prop_a = [
            VarProperty(),
            VarProperty(),
            VarProperty(),
        ]

        self.var_prop_b = set(self.var_prop_a)

        self.var_prop_c = {
            "1": self.var_prop_a[0],
            "2": self.var_prop_a[1],
            "3": self.var_prop_a[2],
        }

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


class TestVariable(unittest.TestCase):
    """Test class"""

    def test_variable(self):
        """Test method"""

        var_prop = VarProperty()
        var = Variable.from_var_property_object(var_prop)
        self.assertEqual(getattr(var, "prop_a"), var_prop.prop_a)
        self.assertEqual(getattr(var, "prop_b"), var_prop.prop_b)
        self.assertEqual(getattr(var, "prop_c"), var_prop.prop_c)
        self.assertFalse(hasattr(var, "prop_d"))

    def test_list_of_variables(self):
        """Test method"""

        var_prop_list = [
            VarProperty(),
            VarProperty(),
            VarProperty(),
        ]
        var_list: List[Any] = Variable.from_var_property_object(var_prop_list)
        self.assertEqual(len(var_prop_list), len(var_list))
        self.assertTrue(isinstance(var_list, list))
        length = len(var_prop_list)
        for i in range(length):
            self.assertEqual(getattr(var_list[i], "prop_a"), var_prop_list[i].prop_a)
            self.assertEqual(getattr(var_list[i], "prop_b"), var_prop_list[i].prop_b)
            self.assertEqual(getattr(var_list[i], "prop_c"), var_prop_list[i].prop_c)
            self.assertFalse(hasattr(var_list[i], "prop_d"))

    def test_set_of_variables(self):
        """Test method"""

        var_prop_list = [
            VarProperty(),
            VarProperty(),
            VarProperty(),
        ]
        var_prop_set = set(var_prop_list)
        var_set: Set[Any] = Variable.from_var_property_object(var_prop_set)
        self.assertEqual(len(var_prop_set), len(var_set))
        self.assertTrue(isinstance(var_set, set))

        index = 0
        for var in var_set:
            self.assertEqual(getattr(var, "prop_a"), var_prop_list[index].prop_a)
            self.assertEqual(getattr(var, "prop_b"), var_prop_list[index].prop_b)
            self.assertEqual(getattr(var, "prop_c"), var_prop_list[index].prop_c)
            self.assertFalse(hasattr(var, "prop_d"))
            index += 1

    def test_dict_of_variables(self):
        """Test method"""

        var_prop_dict = {
            "1": VarProperty(),
            "2": VarProperty(),
            "3": VarProperty(),
        }
        var_dict: Dict[Any, Any] = Variable.from_var_property_object(var_prop_dict)
        self.assertEqual(len(var_prop_dict), len(var_dict))
        self.assertTrue(isinstance(var_dict, dict))

        for key, var in var_dict.items():
            self.assertEqual(getattr(var, "prop_a"), var_prop_dict[key].prop_a)
            self.assertEqual(getattr(var, "prop_b"), var_prop_dict[key].prop_b)
            self.assertEqual(getattr(var, "prop_c"), var_prop_dict[key].prop_c)
            self.assertFalse(hasattr(var, "prop_d"))

    def test_object(self):
        """Test method"""

        var_prop = VarProperty()
        var: Variable = Variable.from_var_property_object(var_prop)
        self.assertFalse(hasattr(var, "prop_d"))
        var.add_object(0, "prop_d")
        self.assertTrue(hasattr(var, "prop_d"))

    def test_complex_variable(self):
        """Test method"""

        complex_var = ComplexVariable()
        var: ComplexVariable = Variable.from_var_property_object(complex_var)
        self.assertTrue(isinstance(var.prop_a, list))
        self.assertTrue(isinstance(var.prop_b, set))
        self.assertTrue(isinstance(var.prop_c, dict))

        length = len(var.prop_a)
        for i in range(length):
            self.assertEqual(getattr(var.prop_a[i], "prop_a"), var.prop_a[i].prop_a)
            self.assertEqual(getattr(var.prop_a[i], "prop_b"), var.prop_a[i].prop_b)
            self.assertEqual(getattr(var.prop_a[i], "prop_c"), var.prop_a[i].prop_c)

        for var_b in var.prop_b:
            self.assertEqual(getattr(var_b, "prop_a"), var.prop_a[0].prop_a)
            self.assertEqual(getattr(var_b, "prop_b"), var.prop_a[0].prop_b)
            self.assertEqual(getattr(var_b, "prop_c"), var.prop_a[0].prop_c)

        for key, var_c in var.prop_c.items():
            self.assertEqual(getattr(var_c, "prop_a"), var.prop_c[key].prop_a)
            self.assertEqual(getattr(var_c, "prop_b"), var.prop_c[key].prop_b)
            self.assertEqual(getattr(var_c, "prop_c"), var.prop_c[key].prop_c)


if __name__ == "__main__":
    unittest.main()
