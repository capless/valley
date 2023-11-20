import collections
from typing import Any, Dict, List, Type

class DeclaredVars(object):
    """
    A class to handle declared variables in a declarative manner.

    Attributes:
        base_field_class (Type[Any]): The base class type for field variables.
    """
    base_field_class: Type[Any] = None

    def get_base_fields(self, bases: tuple, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collects and returns base fields from the given attributes and bases.

        Args:
            bases (tuple): A tuple of base classes.
            attrs (Dict[str, Any]): A dictionary of attributes.

        Returns:
            Dict[str, Any]: A dictionary of base field properties.
        """
        # Collect keys to move to properties without mutating attrs during iteration
        keys_to_move: List[str] = [name for name, obj in attrs.items() if isinstance(obj, self.base_field_class)]

        # Safely populate properties without mutating attrs during iteration
        properties: Dict[str, Any] = {name: attrs.pop(name) for name in keys_to_move}

        # Loop over bases and update properties
        for base in bases:
            base_properties: Dict[str, Any] = getattr(base, '_base_properties', {})
            if base_properties:
                properties.update(base_properties)

        return properties


class DeclarativeVariablesMetaclass(type):
    """
    A metaclass for handling declarative variables.

    Attributes:
        declared_vars_class (Type[DeclaredVars]): The declared variables class.
    """
    declared_vars_class: Type[DeclaredVars] = None

    def __new__(cls, name: str, bases: tuple, attrs: Dict[str, Any]) -> Type:
        """
        Creates a new class instance with base properties.

        Args:
            name (str): The name of the class.
            bases (tuple): A tuple of base classes.
            attrs (Dict[str, Any]): A dictionary of attributes.

        Returns:
            Type: The newly created class.
        """
        attrs['_base_properties'] = cls.declared_vars_class().get_base_fields(bases, attrs)
        new_class: Type = super(DeclarativeVariablesMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class

    @classmethod
    def __prepare__(mcls, cls: str, bases: tuple) -> collections.OrderedDict:
        """
        Prepares the class namespace.

        Args:
            cls (str): The name of the class.
            bases (tuple): A tuple of base classes.

        Returns:
            collections.OrderedDict: An ordered dictionary for the class namespace.
        """
        return collections.OrderedDict()
