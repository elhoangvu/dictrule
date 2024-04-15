"""Join block rule module"""

from typing import (
    Dict,
    Any,
    Callable,
    Optional,
)

from .block_rule import BlockRule
from ..dr_property import dr_property
from ..context import Context
from ..exceptions import (
    InvalidTypeException,
)


class JoinBlockRule(BlockRule):
    """This rule joins generated texts for a block of rules by a specified separator.

    Examples:
    ---------
    >>> dictrule.Generator({
    ...     "join": "-"
    ...     "block": ["This", "is", "the", "snake", "line"]
    ... }).generate()
    This-is-the-snake-line
    """

    @dr_property()
    def _join(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `join` attribute."""

    @dr_property()
    def _block(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `block` attribute."""

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parses the rule dictionary and returns the parsed block of text.

        Args:
            rule_dict (Dict[str, Any]): The rule dictionary to parse.
            rule_callback (Callable[[Optional[Context], Any], str]): A callback function
                to apply to each rule.
            context (Optional[Context], optional): The context to use during parsing.
                Defaults to None.

        Returns:
            str: The parsed block of text.
        """

        _, join = self._join(rule_dict)
        if not isinstance(join, str):
            raise InvalidTypeException("`join` must be a str")

        block = super().internal_parse(
            rule_dict=rule_dict,
            rule_callback=rule_callback,
            separator=join,
            context=context,
        )

        return block
