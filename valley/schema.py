import json
from typing import Any, Dict

from valley.declarative import DeclaredVars as DV, \
    DeclarativeVariablesMetaclass as DVM
from valley.exceptions import ValidationException
from valley.properties import BaseProperty


class BaseSchema:
    """
    Base class for all Valley Schema classes.

    This class provides the basic functionality for schema validation, data serialization, and attribute management.

    Attributes:
        _data (Dict[str, Any]): Stores the data associated with the schema's properties.
        _errors (Dict[str, str]): Stores any validation errors.
        _is_valid (bool): Indicates whether the schema is valid.
        cleaned_data (Dict[str, Any]): Stores the cleaned data after validation.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes a new instance of the BaseSchema.

        Args:
            **kwargs: Arbitrary keyword arguments that represent the schema properties.
        """
        self._data: Dict[str, Any] = {}
        self._errors: Dict[str, str] = {}
        self._is_valid: bool = False
        self.cleaned_data: Dict[str, Any] = {}
        self._init_schema(kwargs)

    def _init_schema(self, kwargs: Dict[str, Any]) -> None:
        """
        Initializes schema properties with provided values or default values.

        Args:
            kwargs (Dict[str, Any]): The keyword arguments for schema properties.
        """
        for key, prop in self._base_properties.items():
            value = kwargs.get(key, prop.get_default_value())
            try:
                self._data[key] = prop.get_python_value(value)
            except ValueError:
                self._data[key] = value

        for i in self.BUILTIN_DOC_ATTRS:
            if i in kwargs:
                self._data[i] = kwargs[i]

    def __getattr__(self, name: str) -> Any:
        """
        Provides dynamic access to schema properties.

        Args:
            name (str): The name of the attribute.

        Returns:
            Any: The value of the schema property.

        Raises:
            AttributeError: If the attribute is not a schema property.
        """
        if name in self._base_properties:
            return self._base_properties[name].get_python_value(self._data.get(name))
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Sets the value for a schema property or a regular attribute.

        Args:
            name (str): The name of the attribute.
            value (Any): The value to set for the attribute.
        """
        if name in self._base_properties:
            self._data[name] = value
        else:
            super().__setattr__(name, value)

    def validate(self) -> None:
        """
        Validates the schema properties against their defined constraints.

        This method updates the _is_valid flag and populates the cleaned_data attribute.
        """
        self._errors = {}
        data = self._data.copy()

        for key, prop in self._base_properties.items():
            value = data.get(key)
            prop_validate = getattr(self, f'{key}_validate', None)

            try:
                prop.validate(value, key)
                if callable(prop_validate):
                    prop_validate(value)
            except ValidationException as e:
                self._handle_validation_error(key, e)

        self._is_valid = not bool(self._errors)
        self.cleaned_data = data

    def _handle_validation_error(self, key: str, error: ValidationException) -> None:
        """
        Handles validation errors either by raising them or storing them in the _errors dictionary.

        Args:
            key (str): The property key associated with the validation error.
            error (ValidationException): The validation exception raised during property validation.
        """
        if self._create_error_dict:
            self._errors[key] = error.error_msg
        else:
            raise error

    def to_json(self) -> str:
        """
        Serializes the schema data to a JSON string.

        Returns:
            str: A JSON string representation of the schema data.
        """
        return json.dumps(self._data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the schema data to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the schema data.
        """
        return self._data


class DeclaredVars(DV):
    """
    A class that stores the schema properties.

    Attributes:
        base_field_class (BaseProperty): The base field class for the schema.
        base_field_type (str): The name of the attribute that stores the schema properties.
    """
    base_field_class = BaseProperty
    base_field_type = '_base_properties'


class DeclarativeVariablesMetaclass(DVM):
    declared_vars_class = DeclaredVars


class Schema(BaseSchema, metaclass=DeclarativeVariablesMetaclass):
    BUILTIN_DOC_ATTRS = []
