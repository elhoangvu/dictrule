"""Inline rule module"""

from typing import (
    Dict,
    Any,
    Callable,
    Optional,
)

from ..rule import Rule
from ..dr_property import dr_property
from ..context import Context
from ..exceptions import (
    InvalidTypeException,
)


class InlineRule(Rule):
    """This rule builds generated text of a list of rules that are in a line.

    Examples:
    ---------
    >>> dictrule.Generator({
    ...    "inline": ["This", " is", " the", " text", " in", " a", " line"]
    ... }).generate()
    This is the text in a line
    """

    @dr_property()
    def _inline(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `inline` attribute."""

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parses the rule dictionary and returns the parsed string.

        Args:
            rule_dict (Dict[str, Any]): The rule dictionary to parse.
            rule_callback (Callable[[Optional[Context], Any], str]): A callback function
                to apply to each rule.
            context (Optional[Context], optional): The context to use during parsing.
                Defaults to None.

        Returns:
            str: The parsed string.
        """

        _, inline = self._inline(rule_dict)
        if not isinstance(inline, list):
            raise InvalidTypeException("`inline` must be a list")

        return "".join([str(rule_callback(context, rule)) for rule in inline])
