"""Format rule module"""

from typing import (
    Dict,
    Any,
    Callable,
    Optional,
)

import re
from enum import Enum
from ..rule import Rule
from ..dr_property import dr_property
from ..context import Context
from ..exceptions import (
    NoneValueException,
    InvalidValueException,
    InvalidTypeException,
)


class FormatRule(Rule):
    """This rule formats text according to specified rules.

    Examples:
    ---------
    >>> dictrule.Generator({
    ...     "format_lowercase": "UPPERCASE TITLE",
    ...     "format_uppercase": "lowercase content",
    ...     "format_upper_head": "camelVariable",
    ...     "format_camel_case": "Camel case",
    ...     "format_pascal_case": "pascal case",
    ...     "format_kabab_case": "Kebab case",
    ...     "format_snake_case": "Snake case",
    ... }).generated()
    uppercase title
    LOWERCASE CONTENT
    CamelVariable
    camelCase
    PascalCase
    kebab-case
    snake_case
    """

    @dr_property(prefix_matching=True)
    def _format(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `format` attribute."""

    class Type(Enum):
        """Enum representing different formatting types for `FormatRule`."""

        LOWERCASE = "lowercase"
        UPPERCASE = "uppercase"
        UPPER_HEAD = "upper_head"
        CAMEL_CASE = "camel_case"
        PASCAL_CASE = "pascal_case"
        KEBAB_CASE = "kebab_case"
        SNAKE_CASE = "snake_case"

        @staticmethod
        def from_str(string: str) -> Optional["FormatRule.Type"]:
            """Creates a `FormatRule.Type` enum from a string.

            Args:
                string (str): The string value representing the formatting type.

            Returns:
                Optional[FormatRule.Type]: The corresponding enum value.
            """

            try:
                return FormatRule.Type(string)
            except ValueError:
                pass

            return None

        def format(
            self,
            text: str,
        ) -> str:
            """Formats the provided text based on the formatting type.

            Args:
                text (str): The text to be formatted.

            Returns:
                str: The formatted text.
            """

            if self == FormatRule.Type.LOWERCASE:
                return text.lower()

            if self == FormatRule.Type.UPPERCASE:
                return text.upper()

            if self == FormatRule.Type.UPPER_HEAD:
                return (text[0].upper() + text[1:]) if len(text) > 0 else ""

            if self == FormatRule.Type.CAMEL_CASE:
                words = list(filter(None, re.split(r"[^a-zA-Z0-9]+", text)))
                return (
                    words[0][0].lower()
                    + (words[0][1:] if len(words[0]) > 0 else "")
                    + "".join(
                        word[0].upper() + (word[1:] if len(word) > 0 else "")
                        for word in words[1:]
                    )
                )

            if self == FormatRule.Type.PASCAL_CASE:
                words = list(filter(None, re.split(r"[^a-zA-Z0-9]+", text)))
                return "".join(
                    word[0].upper() + (word[1:] if len(word) > 0 else "")
                    for word in words
                )

            if self == FormatRule.Type.KEBAB_CASE:
                kebab_text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
                return kebab_text

            if self == FormatRule.Type.SNAKE_CASE:
                snake_text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
                return snake_text

            return text

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parses the format rule and applies formatting to the provided text.

        Args:
            rule_dict (Dict[str, Any]): The dictionary containing the format rule.
            rule_callback (Callable[[Optional[Context], Any], str]): A callback function
                for processing rules.
            context (Optional[Context], optional): The context for the rule. Defaults to None.

        Returns:
            str: The formatted text.
        """

        format_name, format_rule = self._format(rule_dict)
        if not format_name.startswith("format_"):
            raise InvalidValueException(f"Invalid format {format_name}")

        format_type = FormatRule.Type.from_str(format_name[len("format_") :])
        if format_type is None:
            raise NoneValueException(
                "`format:` type {format_type} in invalid with format {format_name}"
            )

        format_text = rule_callback(
            context,
            format_rule,
        )

        if not isinstance(format_text, str):
            raise InvalidTypeException(
                f"`format:` text {format_text} for rule {format_rule} must be a str"
            )

        return format_type.format(format_text)
