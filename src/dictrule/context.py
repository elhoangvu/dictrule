"""Module defines context for rule generation"""

from typing import (
    List,
    Dict,
    Optional,
)

from abc import (
    ABC,
)

from .exceptions import (
    InvalidValueException,
)


class Context:
    """Context class contains information for rule generation"""

    class Case(ABC):
        """Base class for each rule, providing information for rule generation"""

        @property
        def name(self) -> str:
            """Getter for case name, matching the defined rule

            Returns:
                str: A rule name
            """

            return ""

    def __init__(
        self,
        cases: List[Case],
    ) -> None:
        """Initialization method of `Context` class

        Args:
            cases (List[Case]): List of `Context.Case` to build the case map
        """

        self._cases = list(cases)
        case_map: Dict[str, Context.Case] = {}
        for case in cases:
            if case.name in case_map:
                raise InvalidValueException(
                    f"Found existed {Context.Case.__name__}: {case.name}"
                )

            case_map[case.name] = case

        self._case_map = case_map

    @property
    def cases(self) -> List[Case]:
        """Getter for `cases` property

        Returns:
            List[Case]: list of cases
        """
        return self._cases

    @property
    def case_map(self) -> Dict[str, Case]:
        """Getter for `case_map` property

        Returns:
            Dict[str, Case]: map of cases [name: str, case: Context.Case]
        """

        return self._case_map

    def get(self, name: str) -> Optional[Case]:
        """Gets the case by name

        Args:
            name (str): Name of the `Context.Case`

        Returns:
            Optional[Case]: `Context.Case` that matches to provided name,
                built from `Context` creation
        """

        return self._case_map.get(name)
