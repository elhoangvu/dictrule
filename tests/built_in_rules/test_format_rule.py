"""FormatRule test"""

import unittest
from dictrule.built_in_rules import FormatRule


class TestFormatRule(unittest.TestCase):
    """Test class"""

    def test_format_lowercase(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_lowercase": "TEXT 123",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "text 123")

    def test_format_uppercase(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_uppercase": "text 123",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "TEXT 123")

    def test_format_upper_head(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_upper_head": "myText 123",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "MyText 123")

    def test_format_camel_case(self):
        """Test method"""

        texts = [
            "My Camel Case 123",
            "My CamelCase 123",
            "MyCamelCase 123",
            "MyCamelCase123",
            "myCamelCase123",
            "My-Camel-Case 123",
            "My-Camel-Case-123",
            "---My---Camel---Case---123---",
            "My_Camel_Case_123",
            "$$My $Camel $Case $123",
            "$$my $camel $case $123",
        ]

        rule = FormatRule()

        for text in texts:
            parsed = rule.parse(
                rule_dict={
                    "format_camel_case": text,
                },
                rule_callback=lambda x, y: y,
            )
            self.assertEqual(parsed, "myCamelCase123")

    def test_format_pascal_case(self):
        """Test method"""

        texts = [
            "My Pascal Case 123",
            "my pascal case 123",
            "My PascalCase 123",
            "MyPascalCase 123",
            "MyPascalCase123",
            "myPascalCase123",
            "My-Pascal-Case 123",
            "My-Pascal-Case-123",
            "---My---Pascal---Case---123---",
            "My_Pascal_Case_123",
            "$$My $Pascal $Case $123",
            "$$my $pascal $case $123",
        ]

        rule = FormatRule()

        for text in texts:
            parsed = rule.parse(
                rule_dict={
                    "format_pascal_case": text,
                },
                rule_callback=lambda x, y: y,
            )
            self.assertEqual(parsed, "MyPascalCase123")

    def test_format_kebab_case(self):
        """Test method"""

        texts = [
            "My Kebab Case 123",
            "my kebab case 123",
            "My-Kebab-Case 123",
            "My-Kebab-Case-123",
            "---My---Kebab---Case---123---",
            "My_Kebab_Case_123",
            "$$My $Kebab $Case $123",
            "$$my $kebab $case $123",
            "my-kebab-case-123",
            "__my-kebab-case-123__",
        ]

        rule = FormatRule()

        for text in texts:
            parsed = rule.parse(
                rule_dict={
                    "format_kebab_case": text,
                },
                rule_callback=lambda x, y: y,
            )
            self.assertEqual(parsed, "my-kebab-case-123")

    def test_format_snake_case(self):
        """Test method"""

        texts = [
            "My Snake Case 123",
            "my snake case 123",
            "My-Snake-Case 123",
            "My-Snake-Case-123",
            "---My---Snake---Case---123---",
            "My_Snake_Case_123",
            "$$My $Snake $Case $123",
            "$$my $snake $case $123",
            "my-snake-case-123",
            "__my-snake-case-123__",
        ]

        rule = FormatRule()

        for text in texts:
            parsed = rule.parse(
                rule_dict={
                    "format_snake_case": text,
                },
                rule_callback=lambda x, y: y,
            )
            self.assertEqual(parsed, "my_snake_case_123")

    def test_format_empty(self):
        """Test method"""

        rule = FormatRule()

        parsed = rule.parse(
            rule_dict={
                "format_uppercase": "",
            },
            rule_callback=lambda x, y: y,
        )
        self.assertEqual(parsed, "")

    def test_format_invalid(self):
        """Test method"""

        rule = FormatRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "format_123": "text",
                },
                rule_callback=lambda x, y: y,
            )

    def test_format_none(self):
        """Test method"""

        rule = FormatRule()

        with self.assertRaises(Exception):
            _ = rule.parse(
                rule_dict={
                    "format_uppercase": None,
                },
                rule_callback=lambda x, y: y,
            )


if __name__ == "__main__":
    unittest.main()
