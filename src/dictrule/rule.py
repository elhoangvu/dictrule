"""Base Rule module"""

from typing import (
    Set,
    Dict,
    Any,
    Callable,
    Optional,
)

from abc import (
    ABC,
    abstractmethod,
)

from .context import Context
from .dr_property import dr_property


class Rule(ABC):
    """Base Rule class for dictrule module"""

    def __init__(self) -> None:
        self._dr_props = set(dr_property.properties(self))
        self._dr_non_optional_props = set(dr_property.properties(self, optional=False))

    @property
    def dr_props(self) -> Set[Callable]:
        """All `dr_property` properties

        Returns:
            Set[Callable]: Set of `dr_property` functions
        """

        return self._dr_props

    @property
    def dr_non_optional_props(self) -> Set[Callable]:
        """Non optional `dr_property` properties

        Returns:
            Set[Callable]: Set of non-optional `dr_property` functions
        """

        return self._dr_non_optional_props

    @abstractmethod
    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context]], "Rule"],
        context: Optional[Context] = None,
    ) -> str:
        """Abstract parse method for Rule

        Args:
            rule_dict (Dict[str, Any]): Dictionay of rules to generate
            rule_callback (Callable[[Optional[Context]], Rule]): rule callback
                for rules not handled by the current rule
            context (Optional[Context], optional): Context for the rule. Defaults to None.

        Returns:
            str: Generated text
        """

        return ""
