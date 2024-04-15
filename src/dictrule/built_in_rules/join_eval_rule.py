"""Join eval rule module"""

from typing import (
    Dict,
    Any,
    Callable,
    Iterable,
    Optional,
)

from .eval_rule import EvalRule
from ..dr_property import dr_property
from ..context import Context
from ..exceptions import (
    InvalidTypeException,
)


class JoinEvalRule(EvalRule):
    """This rule joins generated texts from the value of `EvalRule` by a specified separator.

    Examples:
    ---------
    >>> context = build_football_teams_context([
    ...     "Real Madrid",
    ...     "Barcelona",
    ...     "Bayern Munchen",
    ...     "PSG",
    ...     "MC",
    ...     "MU",
    ...     "AC Milan",
    ... ])
    >>> dictrule.Generator({
    ...     "join": ", "
    ...     "eval": "football_teams"
    ... }).generate(context)
    Real Madrid, Barcelona, Bayern Munchen, PSG, MC, MU, AC Milan
    """

    @dr_property()
    def _join(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `join` attribute."""

    @dr_property()
    def _eval(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `eval` attribute."""

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

        _, separator = self._join(rule_dict)
        if not isinstance(separator, str):
            raise InvalidTypeException("`join` must be a str")

        eval_rule = super().internal_parse(
            rule_dict=rule_dict,
            rule_callback=rule_callback,
            context=context,
        )

        if not isinstance(eval_rule, Iterable):
            raise InvalidTypeException("`join:eval:` must be a Iterable value")

        return separator.join(eval_rule)
