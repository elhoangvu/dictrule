"""Block rule module"""

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


class BlockRule(Rule):
    """This rule joins a list of rules separated by a new line.

    Examples:
    ---------
    >>> dictrule.Generator({
    ...   "block": [
    ...         "rule_1",
    ...         "rule_2",
    ...         "rule_3",
    ...     ]
    ... }).generate()
    rule_1
    rule_2
    rule_3
    """

    @dr_property()
    def _block(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `block` attribute."""

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parse the rule dictionary.

        Args:
            rule_dict (Dict[str, Any]): A dictionary of rules.
            rule_callback (Callable[[Optional[Context], Any], str]): Callback function
                for rules not handled by the current rule.
            context (Optional[Context], optional): Context for the rule. Defaults to None.

        Returns:
            str: The generated text.
        """

        return self.internal_parse(
            rule_dict=rule_dict,
            rule_callback=rule_callback,
            separator="\n",
            context=context,
        )

    def internal_parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        separator: str,
        context: Optional[Context] = None,
    ) -> str:
        """Internal parse method supporting custom separators instead of the new line as default.

        Args:
            rule_dict (Dict[str, Any]): Dictionary of rules to generate.
            rule_callback (Callable[[Optional[Context], Any], str]): Rule callback
                for rules not handled by the current rule.
            separator (str): Separator for each parsed rule from `rule_dict`.
            context (Optional[Context], optional): Context for the rule. Defaults to None.

        Returns:
            str: The generated text.
        """

        _, block = self._block(rule_dict)
        if not isinstance(block, list):
            raise InvalidTypeException("`block` value must be a list")

        return separator.join([str(rule_callback(context, rule)) for rule in block])
