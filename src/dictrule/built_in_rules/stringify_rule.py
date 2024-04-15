"""Stringify rule module"""

from typing import (
    Dict,
    Any,
    Callable,
    Optional,
)

from ..rule import Rule
from ..dr_property import dr_property
from ..context import Context


class StringifyRule(Rule):
    """This rule wraps content by quotes.

    Examples:
    ---------
    >>> dictrule.Generator({
    ...    "stringify": "This is the 1st text"
    ...    "stringify": "This is the 2nd text"
    ... }).generate()
    "This is the 1st text"
    "This is the 2nd text"
    """

    QUOTE = '"'

    @dr_property()
    def _stringify(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `stringify` attribute."""

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Stringify a text by enclosing it with specified quotes.

        Args:
            rule_dict (Dict[str, Any]): The rule dictionary to parse.
            rule_callback (Callable[[Optional[Context], Any], str]): A callback function
                to apply to each rule.
            context (Optional[Context], optional): The context to use during parsing.
                Defaults to None.

        Returns:
            str: The parsed string.
        """

        _, stringify = self._stringify(rule_dict)
        value = stringify
        if not isinstance(value, str):
            value = rule_callback(context, value)

        if value is None:
            value = ""

        return StringifyRule.QUOTE + str(value) + StringifyRule.QUOTE
