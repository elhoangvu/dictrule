"""For-in rule module"""

from typing import (
    Dict,
    List,
    Iterable,
    Any,
    Callable,
    Optional,
)

from .eval_rule import EvalRule
from .block_rule import BlockRule
from ..rule import Rule
from ..dr_property import dr_property
from ..context import Context
from ..exceptions import (
    NoneValueException,
    InvalidTypeException,
)


class ForInRule(Rule):
    """This rule executes generatable rules in a `for-in-block` loop
    with a provided iterable variable.

    Requires providing a `Context` that includes the necessary information
    for the rules in the `block`.

    The `in` keyword must be represented by a `EvalRule` variable,
    and the value of this variable must be a `Interable` type.

    Examples:
    ---------
    >>> context = build_saved_lines_context([
    ...     Line(content="This is the line_1 content"),
    ...     Line(content="This is the line_2 content"),
    ... ])
    >>> dictrule.Generator({
    ...     "for": "line"
    ...     "in": "saved_lines"
    ...     "block: [
    ...         "line.index",
    ...         "line.content"
    ...     ]
    ... }).generate()
    1
    This is the line_1 content
    2
    This is the line_2 content
    """

    @dr_property()
    def _for(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `for` attribute."""

    @dr_property()
    def _in(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `in` attribute."""

    @dr_property()
    def _block(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `block` attribute."""

    class ForInEval(EvalRule.Evaluable):
        """Rule for executing generable rules in a `for-in-eval` loop.

        Examples:
        ---------
        command_list = [
            "This Is The Title",
            "and this is the description",
            "are_created_at",
            "2024-01-01",
        ]

        >>> rule_dict = {
        ...     "for": "command",
        ...     "in": "command_list",
        ...     "eval": "command",
        ... }
        This Is The Title
        and this is the description
        are_created_at
        2024-01-01
        """

        @property
        def name(self) -> str:
            """Getter for `name` property"""

            return self._var_name

        @property
        def prefix_matching(self) -> bool:
            """Getter for `prefix_matching` property"""

            return True

        def __init__(
            self,
            var_name: str,
            var: Any,
            extra_properties: Dict[str, Any],
        ):
            """Initializes the ForInEval object.

            Args:
                var_name (str): The name of the variable in the rule dictionary.
                var (Any): The name of the executable variable.
                extra_properties (Dict[str, Any]): A map of variable names and values.
            """

            self._var_name = str(var_name)
            self._var = var
            self._extra_properties = dict(extra_properties)

        def run(
            self,
            cmd: str,
        ) -> str:
            """Executes the evaluable rule.

            This method runs the evaluable rule based on the provided command.

            Args:
                cmd (str): The command to be executed.

            Returns:
                str: The result of the execution.
            """

            var_prefix = self._var_name + "."
            if not cmd.startswith(var_prefix):
                return self._var

            properties = cmd.split(".")
            property_value = ""
            extra_prop = ".".join(properties[1:])
            if extra_prop in self._extra_properties:
                property_value = self._extra_properties[extra_prop]
            else:
                local_var = self._var
                for prop in properties[1:]:
                    callable_var = getattr(local_var, prop)
                    if callable(callable_var):
                        local_var = callable_var(local_var)
                    else:
                        local_var = callable_var

                property_value = local_var

            return property_value

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parses the rule dictionary for `ForInRule`.

        Args:
            rule_dict (Dict[str, Any]): Dictionary of rules containing `ForInRule`.
            rule_callback (Callable[[Optional[Context], Any], str]): Fallback for other rules.
            context (Optional[Context], optional): `ForInRule` context. Defaults to None.

        Returns:
            str: Parsed value for `rule_dict`.
        """

        if context is None:
            raise NoneValueException("param `context` must not be None")

        _, for_var = self._for(rule_dict)
        _, in_var = self._in(rule_dict)
        _, block = self._block(rule_dict)

        if not isinstance(for_var, str):
            raise InvalidTypeException(f"`for:` {for_var} must be a str")

        if not isinstance(in_var, str):
            raise InvalidTypeException(f"`for:in:` {in_var} must be a str")

        if not isinstance(block, List):
            raise InvalidTypeException(f"`for:block:` {block} must be a list")

        eval_in = EvalRule().internal_parse(
            rule_dict={
                "eval": in_var,
            },
            context=context,
            rule_callback=rule_callback,
        )

        if not isinstance(eval_in, Iterable):
            raise InvalidTypeException("`in` must return an Iterable value")

        blocks: List[str] = []
        case_map = dict(context.case_map)
        eval_context_case: EvalRule.ContextCase = case_map.get(EvalRule.CONTEXT_NAME)
        is_eval_context_case = isinstance(eval_context_case, EvalRule.ContextCase)
        case_map.pop(EvalRule.CONTEXT_NAME)
        without_eval_cases = list(case_map.values())
        for index, var in enumerate(eval_in):
            block_context = Context(
                without_eval_cases
                + [
                    EvalRule.ContextCase(
                        evaluators=(
                            eval_context_case.evaluator_list
                            if is_eval_context_case
                            else []
                        )
                        + [
                            ForInRule.ForInEval(
                                var_name=for_var,
                                var=var,
                                extra_properties={
                                    "index": index,
                                },
                            )
                        ],
                        fallback=(
                            eval_context_case.fallback if is_eval_context_case else None
                        ),
                    ),
                ],
            )

            block_parsed = BlockRule().parse(
                rule_dict={
                    "block": block,
                },
                rule_callback=rule_callback,
                context=block_context,
            )

            blocks.append(block_parsed)

        return "\n".join(blocks)
