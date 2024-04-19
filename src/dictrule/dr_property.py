"""dr_property decorator module"""

import functools
from typing import (
    List,
    Dict,
    Any,
    Callable,
    Optional,
)

from .exceptions import (
    InvalidTypeException,
)


class dr_property:
    """dictrule decorator that defines property for rules.
    Supports prefix matching and optional properties

    Properties decorated with `dr_property` must have the `dr_property._prefix` prefix.

    Examples:
    ---------
    >>> rule_dict = {
    ...     "eval": "prop.name"
    ... }
    >>> @dr_property(prefix_matching=True, optional=True)
    ... def _eval(self, props: Dict[str, Any]) -> Any:
    ...     pass
    >>> key, value = self._eval(rule_dict)
    >>> print(key)
    eval
    >>> print(value)
    prop.name
    """

    _prefix = "_"
    _flag_key = "_is_dr_property"
    _name_key = "_dr_name"
    _optional_key = "_dr_optional"

    def __init__(
        self,
        optional: bool = False,
        prefix_matching: bool = False,
    ):
        """Initialization method of `dr_property`

        Args:
            optional (bool, optional): Indicates if the property is optional
                and used for detecting rules. Defaults to False.
            prefix_matching (bool, optional): Indicates if the property matches the rule prefix.
                Defaults to False.
        """

        self._optional = optional
        self._prefix_matching = prefix_matching

    def __call__(
        self,
        *args,
        **kwds,
    ) -> Optional[Any]:
        func = args[0]
        key = func.__name__[len(dr_property._prefix) :]
        setattr(func, dr_property._flag_key, True)
        setattr(func, dr_property._name_key, key)
        setattr(func, dr_property._optional_key, self._optional)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_value = func(*args, **kwargs)
            if func_value:
                return func_value

            props: Dict[str, Any] = args[1]
            if not isinstance(props, Dict):
                raise InvalidTypeException(f"First param `{props}` must be a dict")

            if self._prefix_matching:
                for prop, value in props.items():
                    if prop.startswith(key):
                        return (prop, value)

            return (key, props.get(key))

        return wrapper

    @classmethod
    def properties(
        cls,
        instance: Any,
        optional: bool = True,
    ) -> List[Callable]:
        """Fetches all `dr_property` of `instance`.

        Args:
            instance (Any): Instance using `dr_property`.
            optional (bool, optional): True if fetching optional `dr_property`. Defaults to True.

        Returns:
            List[Callable]: List of `dr_property` functions
        """
        properties: List[Callable] = []
        for name in dir(instance):
            attr = getattr(instance, name, None)
            is_tg = getattr(attr, cls._flag_key, None)
            if not is_tg:
                continue

            if not optional:
                is_optional = getattr(attr, cls._optional_key, None)
                if is_optional:
                    continue

            properties.append(attr)
        return properties

    @classmethod
    def str_properties(
        cls,
        instance: Any,
        optional: bool = True,
    ) -> List[str]:
        """Fetches all `dr_property` of `instance` as list of strings.

        Args:
            instance (Any): Instance using `dr_property`
            optional (bool, optional): True if fetching optional `dr_property`. Defaults to True.

        Returns:
            List[Callable]: List of `dr_property` strings.
        """
        return [
            getattr(prop, dr_property._name_key)
            for prop in cls.properties(
                instance=instance,
                optional=optional,
            )
        ]
