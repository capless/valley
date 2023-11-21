import json
from collections.abc import Callable
from typing import Any, Optional, Type, List

from valley.utils.json_utils import ValleyEncoder
from .validators import (
    RequiredValidator, StringValidator, MaxLengthValidator, MinLengthValidator,
    IntegerValidator, MaxValueValidator, MinValueValidator, FloatValidator,
    DateValidator, DateTimeValidator, BooleanValidator, SlugValidator,
    EmailValidator, DictValidator, ChoiceValidator, ListValidator,
    ForeignValidator, ForeignListValidator, MultiValidator
)

__all__ = [
    'BaseProperty', 'StringProperty', 'IntegerProperty', 'FloatProperty',
    'BooleanProperty', 'DateProperty', 'DateTimeProperty', 'SlugProperty',
    'EmailProperty', 'DictProperty', 'ListProperty', 'ForeignProperty',
    'ForeignListProperty', 'MultiProperty'
]

class BaseProperty:
    """
    Base class for defining properties in the Valley library.

    Attributes:
        default_value (Any): The default value for the property.
        required (bool): Indicates whether the property is required.
        validators (List[Callable]): A list of validators for the property.
        choices (Optional[List[Any]]): A list of choices for the property value.
        kwargs (dict): Additional keyword arguments.

    """
    default_value: Any = None
    allow_required: bool = True

    def __init__(self, default_value: Any = None, required: bool = False,
                 validators: Optional[List[Callable]] = None,
                 choices: Optional[List[Any]] = None, **kwargs):
        self.default_value = default_value
        self.required = required
        self.validators = validators if validators is not None else []
        self.choices = choices
        self.kwargs = kwargs
        self.get_validators()

    def get_validators(self) -> None:
        """
        Initialize the validators for the property based on its configuration.
        """
        if self.required:
            self.validators.insert(0, RequiredValidator())
        if self.choices:
            self.validators.insert(0, ChoiceValidator(self.choices))

    def validate(self, value: Any, key: str) -> None:
        """
        Validate the value of the property.

        Args:
            value (Any): The value to be validated.
            key (str): The key associated with the property.

        Raises:
            ValidationException: If the value does not pass the validation checks.
        """
        if not value and not isinstance(self.get_default_value(), type(None)):
            value = self.get_default_value()
        for validator in self.validators:
            validator.validate(value, key)

    def get_default_value(self) -> Any:
        """
        Get the default value of the property.

        Returns:
            Any: The default value.
        """
        default = self.default_value
        if isinstance(default, Callable):
            default = default()
        return default

    def get_db_value(self, value: Any) -> Any:
        """
        Get the database value of the property.

        Args:
            value (Any): The value to be converted.

        Returns:
            Any: The converted value suitable for database storage.
        """
        if not value:
            return
        return value

    def get_python_value(self, value: Any) -> Any:
        """
        Get the Python value of the property.

        Args:
            value (Any): The value to be converted.

        Returns:
            Any: The converted value suitable for Python.
        """
        return value


class StringProperty(BaseProperty):
    """
    A property that represents a string value.

    Inherits from BaseProperty and adds string-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the CharProperty.
        """
        super().get_validators()
        self.validators.append(StringValidator())
        if 'min_length' in self.kwargs:
            self.validators.append(MinLengthValidator(self.kwargs['min_length']))
        if 'max_length' in self.kwargs:
            self.validators.append(MaxLengthValidator(self.kwargs['max_length']))

    def get_python_value(self, value: Any) -> Optional[str]:
        """
        Convert the value to a string if it is not None.

        Args:
            value (Any): The value to be converted.

        Returns:
            Optional[str]: The converted value as a string or None.
        """
        if value is not None:
            return str(value)
        return value


class IntegerProperty(BaseProperty):
    """
    A property that represents an integer value.

    Inherits from BaseProperty and adds integer-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the IntegerProperty.
        """
        super().get_validators()
        self.validators.append(IntegerValidator())
        if 'min_value' in self.kwargs:
            self.validators.append(MinValueValidator(self.kwargs['min_value']))
        if 'max_value' in self.kwargs:
            self.validators.append(MaxValueValidator(self.kwargs['max_value']))


class FloatProperty(BaseProperty):
    """
    A property that represents a floating-point value.

    Inherits from BaseProperty and adds float-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the FloatProperty.
        """
        super().get_validators()
        self.validators.append(FloatValidator())


class BooleanProperty(BaseProperty):
    """
    A property that represents a boolean value.

    Inherits from BaseProperty and adds boolean-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the BooleanProperty.
        """
        super().get_validators()
        self.validators.append(BooleanValidator())

    def get_default_value(self) -> bool:
        """
        Get the default value of the BooleanProperty.

        Returns:
            bool: The default boolean value.
        """
        default = self.default_value
        return bool(default)


class DateProperty(BaseProperty):
    """
    A property that represents a date value.

    Inherits from BaseProperty and adds date-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the DateProperty.
        """
        super().get_validators()
        self.validators.append(DateValidator())


class DateTimeProperty(BaseProperty):
    """
    A property that represents a datetime value.

    Inherits from BaseProperty and adds datetime-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the DateTimeProperty.
        """
        super().get_validators()
        self.validators.append(DateTimeValidator())


class SlugProperty(StringProperty):
    """
    A property that represents a slug (URL-friendly string).

    Inherits from CharProperty and adds slug-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the SlugProperty.
        """
        super().get_validators()
        self.validators.append(SlugValidator())

    def get_python_value(self, value: Any) -> Optional[str]:
        """
        Convert the value to a slug string if it is not None.

        Args:
            value (Any): The value to be converted.

        Returns:
            Optional[str]: The converted value as a slug string or None.
        """
        if value is not None:
            return str(value)
        return value


class EmailProperty(BaseProperty):
    """
    A property that represents an email address.

    Inherits from BaseProperty and adds email-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the EmailProperty.
        """
        super().get_validators()
        self.validators.append(EmailValidator())


class DictProperty(BaseProperty):
    """
    A property that represents a dictionary.

    Inherits from BaseProperty and adds dictionary-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the DictProperty.
        """
        super().get_validators()
        self.validators.append(DictValidator())


class ListProperty(BaseProperty):
    """
    A property that represents a list.

    Inherits from BaseProperty and adds list-specific validators.
    """

    def get_validators(self) -> None:
        """
        Initialize the validators for the ListProperty.
        """
        super().get_validators()
        self.validators.append(ListValidator())


class ForeignProperty(BaseProperty):
    def __init__(self, foreign_class: Type, return_type: str = 'single', return_prop: Optional[str] = None,
                 **kwargs: Any):
        """
        Initialize a ForeignProperty.

        Args:
            foreign_class (Type): The class of the foreign object.
            return_type (str, optional): The type of return value. Defaults to 'single'.
            return_prop (Optional[str], optional): The property name to return. Required if return_type is 'single'. Defaults to None.
            **kwargs: Additional keyword arguments.
        """
        self.foreign_class = foreign_class
        self.return_type = return_type
        self.return_prop = return_prop
        super().__init__(**kwargs)

    def get_validators(self) -> None:
        """
        Get validators for the foreign property, adding ForeignValidator to the list.
        """
        super().get_validators()
        self.validators.insert(0, ForeignValidator(self.foreign_class))

    def get_db_value(self, value: Any) -> Any:
        """
        Get the database value for the property.

        Args:
            value (Any): The value to be processed.

        Returns:
            Any: The processed value.
        """
        if not value:
            return None
        if self.return_type == 'single':
            if not self.return_prop:
                raise ValueError('ForeignProperty requires the return_prop argument if return_type is "single"')
            return value._data[self.return_prop]
        if self.return_type == 'dict':
            return value._data
        if self.return_type == 'json':
            return json.dumps(value, cls=ValleyEncoder)
        else:
            return value


class ForeignListProperty(ListProperty):
    def __init__(self, foreign_class: Type, **kwargs: Any):
        """
        Initialize a ForeignListProperty.

        Args:
            foreign_class (Type): The class of the foreign object.
            **kwargs: Additional keyword arguments.
        """
        self.foreign_class = foreign_class
        super().__init__(**kwargs)

    def get_validators(self) -> None:
        """
        Get validators for the foreign list property, adding ForeignListValidator to the list.
        """
        super().get_validators()
        self.validators.insert(len(self.validators), ForeignListValidator(self.foreign_class))

    def get_db_value(self, value: Any) -> Any:
        """
        Get the database value for the list property.

        Args:
            value (Any): The value to be processed.

        Returns:
            Any: The processed value.
        """
        if not value:
            return None
        if self.return_type == 'list':
            return [obj._data for obj in value]
        if self.return_type == 'json':
            return json.dumps(value, cls=ValleyEncoder)
        else:
            return value


class MultiProperty(BaseProperty):
    def get_validators(self) -> None:
        """
        Get validators for the multi property, encapsulating existing validators in a MultiValidator.
        """
        super().get_validators()
        self.validators = [MultiValidator(self.validators)]
