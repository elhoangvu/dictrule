"""Variable module"""

from typing import (
    Any,
    List,
    Dict,
    Set,
    Optional,
)

from .var_property import var_property


class Variable:
    """Parses instances with nested values.

    Supported value types:
    - An item in Variable.PRIMITIVE_TYPES: [
        int,
        float,
        str,
    ]
    - list
    - set
    - dict
    - Variable

    Examples:
    ---------
    >>> class Sample:
    ...     @var_property
    ...     def name(self) -> str:
    ...         return "Zooxy"
    ...     def age(self) -> int:
    ...         return 20
    >>> var = Variable.from_var_property_object(Sample())
    >>> print(var.name)
    Zooxy
    >>> print(hasattr(var, "age"))
    False
    """

    PRIMITIVE_TYPES = set(
        [
            int,
            float,
            str,
        ]
    )

    @staticmethod
    def from_var_property_object(
        obj: Any,
    ) -> "Variable":
        """Parses a Variable from obj where properties are decorated with @var_property.

        Args:
            obj (Any): The object to parse from @var_property and supported values.

        Returns:
            Variable: The parsed variable.
        """

        return Variable._parse_value(obj)

    def add_object(
        self,
        obj: Any,
        name: str,
    ):
        """Adds a new object to the Variable instance with a given name.

        Args:
            obj (Any): The object to be added.
            name (str): The name for the object.
        """

        value = self._parse_value(obj)
        setattr(self, name, value)

    @staticmethod
    def _parse_value(
        value: Any,
    ) -> Optional[Any]:
        """Parses supported values.

        Args:
            value (Any): The supported value.

        Returns:
            Optional[Any]: The parsed value.
        """

        if value is None:
            return

        parsed_value = None
        if type(value) in Variable.PRIMITIVE_TYPES or isinstance(value, Variable):
            parsed_value = value
        elif isinstance(value, list):
            parsed_value = Variable._parse_list(
                value=value,
            )
        elif isinstance(value, set):
            parsed_value = Variable._parse_set(
                value=value,
            )
        elif isinstance(value, dict):
            parsed_value = Variable._parse_dict(
                value=value,
            )
        else:
            attrs = var_property.properties(value)
            if not attrs:
                return None

            parsed_value = Variable()
            for attr in attrs:
                setattr(parsed_value, attr.__name__, attr.__get__(value))

        return parsed_value

    @staticmethod
    def _parse_list(
        value: List[Any],
    ):
        """Parses a list value.

        Args:
            value (List[Any]): The list of values.

        Returns:
            Optional[List[Any]]: The parsed list.
        """

        new_list: List[Any] = []
        for v in value:
            parsed_value = Variable._parse_value(v)
            if parsed_value:
                new_list.append(parsed_value)
        return new_list

    @staticmethod
    def _parse_set(
        value: Set[Any],
    ):
        """Parses a set value.

        Args:
            value (Set[Any]): The set of values.

        Returns:
            Optional[Set[Any]]: The parsed set.
        """

        new_set: Set[Any] = set()
        for v in value:
            parsed_value = Variable._parse_value(v)
            if not parsed_value:
                continue

            new_set.add(parsed_value)

        return new_set

    @staticmethod
    def _parse_dict(
        value: Dict[Any, Any],
    ):
        """Parses a dictionary value.

        Args:
            value (Dict[Any, Any]): The dictionary of values.

        Returns:
            Optional[Dict[str, Any]]: The parsed dictionary.
        """

        new_dict: Dict[str, Any] = {}
        for k, v in value.items():
            parsed_key = Variable._parse_value(k)
            if not parsed_key:
                continue

            parsed_value = Variable._parse_value(v)
            if not parsed_value:
                continue

            new_dict[parsed_key] = parsed_value

        return new_dict
