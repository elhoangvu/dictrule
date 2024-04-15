"""Indent rule module"""

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
    NoneValueException,
    InvalidValueException,
    InvalidTypeException,
)


class IndentRule(Rule):
    """This rule indents generated text from provided rules by a specified number of indent spaces.

    Defines the number of spaces for text indentation by providing `IndentRule.ContextCase`
    within the `Context`.

    Examples:
    ---------
    >>> context = build_number_spaces_context(4)
    >>> dictrule.Generator({
    ...     "class Menu:"
    ...     "indent_1": "def content(self):"
    ...     "indent_2": "return 'Empty'"
    ... }).generate(context)
    class Menu:
        def content(self):
            return 'Empty'
    """

    DEFAULT_SPACES = 2
    CONTEXT_NAME = "indent"

    class ContextCase(Context.Case):
        """`Context.Case` for `IndentRule`."""

        @property
        def name(self) -> str:
            """Getter for `name` property"""

            return "indent"

        def __init__(
            self,
            num_spaces: int,
        ):
            """Initializes the context case.

            Args:
                num_spaces (int): The number of spaces for each level of indentation.
            """

            self._num_spaces = num_spaces

        @property
        def num_spaces(self) -> int:
            """Getter for `num_spaces` property"""

            return self._num_spaces

    @dr_property(prefix_matching=True)
    def _indent(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `indent` attribute."""

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parses the indent rule and applies indentation to the provided text.

        Args:
            rule_dict (Dict[str, Any]): The dictionary containing the indent rule.
            rule_callback (Callable[[Optional[Context], Any], str]): A callback function
                for processing rules.
            context (Optional[Context], optional): The context for the rule. Defaults to None.

        Returns:
            str: The indented text.
        """

        if context is None:
            raise NoneValueException("param `context` must not be None")

        context_case: IndentRule.ContextCase = context.get(IndentRule.CONTEXT_NAME)

        indent_spaces = IndentRule.DEFAULT_SPACES
        if context_case:
            if not isinstance(context_case, IndentRule.ContextCase):
                raise InvalidTypeException(
                    f"Invalid {type(context_case)} type for {IndentRule.CONTEXT_NAME} in context"
                )

            indent_spaces = context_case.num_spaces

        indent, value = self._indent(rule_dict)
        if not indent.startswith("indent_"):
            raise InvalidValueException(f"Invalid indent {indent}")

        if not indent_spaces or indent_spaces <= 0:
            indent_spaces = IndentRule.DEFAULT_SPACES

        if not isinstance(indent_spaces, int) and not (
            isinstance(indent_spaces, str) and str.isdigit(indent_spaces)
        ):
            raise InvalidTypeException("`indent_spaces` must be a digit")

        indent_spaces: int = int(indent_spaces)

        if not indent_spaces:
            print("`indent_spaces` is not found in `context`, using default spaces")
            indent_spaces = 4

        if not isinstance(value, str):
            value = rule_callback(context, value)

        indent_prefix = indent_spaces
        if indent != "indent":
            indent_count = indent[len("indent_") :]
            if not indent_count.isdigit():
                raise InvalidValueException("`indent_` suffix must be a digit str")

            indent_prefix = indent_spaces * int(indent_count) * " "

        value = indent_prefix + value.replace("\n", f"\n{indent_prefix}")
        return value
