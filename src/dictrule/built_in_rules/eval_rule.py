"""Eval rule module"""

from typing import (
    Dict,
    List,
    Any,
    Callable,
    Optional,
)

from abc import ABC, abstractmethod
from functools import lru_cache
from ..rule import Rule
from ..dr_property import dr_property
from ..context import Context
from ..exceptions import (
    NoneValueException,
    InvalidTypeException,
)


class EvalRule(Rule):
    """This rule evaluates the value of provied variable or command.

    Examples:
    ---------
    >>> git_author = "Zooxy Le"
    >>> dictrule.Generator({
    ...     "eval": "git_author"
    ... }).generate()
    Zooxy Le

    >>> project_id = "123456789"
    >>> dictrule.Generator({
    ...     "eval": "project_id"
    ... }).generate()
    123456789
    """

    CONTEXT_NAME = "eval"

    @dr_property()
    def _eval(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `eval` attribute."""

    class Evaluable(ABC):
        """Abstract class for the evaluator."""

        @property
        def name(self) -> str:
            """Name or command for evaluator"""

            return EvalRule.CONTEXT_NAME

        @property
        def prefix_matching(self) -> bool:
            """`prefix_matching` property defines evaluator should use prefix for matching name"""
            return False

        @abstractmethod
        def run(
            self,
            cmd: str,
        ) -> Any:
            """Run `cmd`

            Args:
                cmd (str): command or variable name to eval the vale

            Returns:
                Any: value of `cmd`
            """

            return None

    class KeyValueEvaluator(Evaluable):
        """Evaluator using key-value pairs."""

        def __init__(
            self,
            key: str,
            value: Any,
        ):
            """Initial method for `KeyValueEvaluator`

            Args:
                key (str): key as name of `Evaluable`
                value (Any): value of eval name
            """

            self._key = key
            self._value = value

        @property
        def name(self) -> str:
            return self._key

        def run(self, cmd: str) -> Any:
            return self._value

    class ContextCase(Context.Case):
        """`Context.Case` for `EvalRule`.

        This class manages contexts for the `EvalRule`,
        including a list of evaluators and fallbacks.

        Attributes:
            name (str): The name of the context, inherited from `Context.Case`.
            evaluator_list (List["EvalRule.Evaluable"]): A list of evaluators.
            fallback (Optional["EvalRule.Evaluable"]): The fallback evaluator for other rules.

        Args:
            evaluators (List["EvalRule.Evaluable"]): The list of evaluators.
            fallback (Optional["EvalRule.Evaluable"], optional): The fallback evaluator
                for other rules. Defaults to None.
        """

        @property
        def name(self) -> str:
            """Getter for `name` property"""

            return EvalRule.CONTEXT_NAME

        @property
        def evaluator_list(self) -> List["EvalRule.Evaluable"]:
            """Getter for `evaluator_list` property"""

            return self._evaluator_list

        @property
        def fallback(self) -> Optional["EvalRule.Evaluable"]:
            """Getter for `fallback` property"""

            return self._fallback

        def __init__(
            self,
            evaluators: List["EvalRule.Evaluable"],
            fallback: Optional["EvalRule.Evaluable"] = None,
        ):
            """Initialization method for `EvalRule.ContextCase`.

            Args:
                evaluators (List["EvalRule.Evaluable"]): List of evaluators.
                fallback (Optional["EvalRule.Evaluable"], optional): Fallback for other rules.
                    Defaults to None.
            """

            self._evaluator_list = list(evaluators)
            self._fallback = fallback
            nonprefix_evaluators: Dict[str, EvalRule.Evaluable] = {}
            prefix_evaluators: Dict[str, EvalRule.Evaluable] = {}

            for evaluator in evaluators:
                if evaluator.prefix_matching:
                    prefix_evaluators[evaluator.name] = evaluator
                else:
                    nonprefix_evaluators[evaluator.name] = evaluator

            self._evaluators = nonprefix_evaluators
            self._prefix_evaluators = prefix_evaluators

        def eval(
            self,
            eval_name: str,
        ) -> Optional[Any]:
            """Evaluates value with name.

            Args:
                eval_name (str): The name for evaluating.

            Returns:
                Optional[Any]: Evaluated value.
            """

            eval_rule = self._evaluators.get(eval_name)
            if not eval_rule:
                eval_rule = self._find_eval_by_prefix(
                    eval_name=eval_name,
                )

            if not eval_rule:
                if self._fallback:
                    return self._fallback.run(eval_name)
                return None

            return eval_rule.run(eval_name)

        @lru_cache(maxsize=1024)
        def _find_eval_by_prefix(
            self,
            eval_name: str,
        ) -> Optional["EvalRule.Evaluable"]:
            """Finds an evaluator by prefix.

            Args:
                eval_name (str): The name for evaluation.

            Returns:
                Optional[EvalRule.Evaluable]: The evaluator found by prefix.
            """

            for name, evaluator in self._prefix_evaluators.items():
                if eval_name.startswith(name):
                    return evaluator

            return None

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parses the rule dictionary for EvalRule.

        Args:
            rule_dict (Dict[str, Any]): Dictionary of rules containing EvalRule.
            rule_callback (Callable[[Optional[Context], Any], str]): Fallback for other rules.
            context (Optional[Context], optional): EvalRule's context. Defaults to None.

        Returns:
            str: Parsed value for `rule_dict`.
        """

        parsed = self.internal_parse(
            rule_dict=rule_dict,
            rule_callback=rule_callback,
            context=context,
        )

        if parsed is None:
            raise NoneValueException(
                f"EvalRule with dict `{rule_dict}` reacts None value"
            )

        return parsed

    def internal_parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> Any:
        """Internal method for parsing rule dictionary for EvalRule.

        Args:
            rule_dict (Dict[str, Any]): Dictionary of rules containing EvalRule.
            rule_callback (Callable[[Optional[Context], Any], str]): Fallback for other rules.
            context (Optional[Context], optional): EvalRule's context. Defaults to None.

        Returns:
            Any: Parsed value for `rule_dict`.
        """

        _ = rule_callback
        if context is None:
            raise NoneValueException("param `context` must not be None")

        context_case: EvalRule.ContextCase = context.get(EvalRule.CONTEXT_NAME)

        if not isinstance(context_case, EvalRule.ContextCase):
            raise InvalidTypeException(
                f"Invalid {type(context_case)} type for {EvalRule.CONTEXT_NAME} in context"
            )

        _, eval_rule = self._eval(rule_dict)
        if not isinstance(eval_rule, str):
            raise InvalidTypeException("`eval` must be a str")

        value = context_case.eval(eval_rule)
        return value
