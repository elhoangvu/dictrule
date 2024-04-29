"""var_property decorator module"""

from typing import (
    List,
    Any,
    Callable,
    Optional,
)


class var_property:
    """var_property decorator that defines property for dictrule.Variable.

    Examples:
    ---------
    >>> class Person:
    ...     @var_property
    ...     def name(self) -> str:
    ...         return "Zooxy"
    ...     def age(self) -> int:
    ...         return 20
    >>> var = dictrule.Variable.from_object(Person())
    >>> print(isinstance(var, Variable))
    True
    >>> print(var.name)
    Zooxy
    >>> print(var.age)
    20
    """

    def __init__(
        self,
        fget: Optional[Callable[[Any], Any]] = None,
        fset: Optional[Callable[[Any, Any], None]] = None,
        fdel: Optional[Callable[[Any], None]] = None,
        doc: Optional[str] = None,
    ):
        """var_property decorator

        Args:
            fget (Optional[Callable[[Any], Any]], optional): Getter method. Defaults to None.
            fset (Optional[Callable[[Any, Any], None]], optional): Setter method. Defaults to None.
            fdel (Optional[Callable[[Any], None]], optional): Delete method. Defaults to None.
            doc (Optional[str], optional): Document string. Defaults to None.
        """

        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self.__name__ = fget.__name__

    def __get__(self, obj, objtype=None) -> Any:
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value) -> None:
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj) -> None:
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget) -> "var_property":
        """Getter decorator

        Examples:
        ---------
        >>> class Sample:
        ...     @var_property
        ...     def name(self):
        ...         return "Zooxy"
        >>> Sample().name
        Zooxy
        """
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset) -> "var_property":
        """Setter decorator

        Examples:
        ---------
        >>> @name.setter
        ... def name(self, value: Any):
        ...     self._name = value
        """
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel) -> "var_property":
        """Deleter decorator

        Examples:
        ---------
        >>> @name.deleter
        ... def name(self):
        ...     del self._name
        """
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

    @classmethod
    def properties(
        cls,
        instance: Any,
    ) -> List[Callable[[Any], Any]]:
        """Fetches all `var_property` of `instance`.

        Args:
            instance (Any): Instance using `var_property`.

        Returns:
            List[Callable]: List of `var_property` functions
        """
        properties: List[Callable] = []
        for name in dir(instance.__class__):
            attr = getattr(instance.__class__, name, None)
            is_prop = isinstance(attr, var_property)
            if not is_prop:
                continue

            properties.append(attr)
        return properties
