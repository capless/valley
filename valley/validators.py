import re
import datetime
import time
from typing import Any, List, Dict, Type, Optional

from valley.exceptions import ValidationException


class Validator:
    """
    Base class for all validators.

    This class provides basic structure and interface for all specific validators.
    """

    def validate(self, value: Any, name: str) -> None:
        """
        Validates the given value.

        Args:
            value (Any): The value to validate.
            name (str): The name of the property being validated.

        Raises:
            ValidationException: If the validation fails.
        """
        raise NotImplementedError


class RequiredValidator(Validator):
    """
    Validator to ensure a value is not None or empty.
    """

    def validate(self, value: Any, name: str) -> None:
        if value is None or value == '':
            raise ValidationException(f'{name} is required and cannot be empty.')


class StringValidator(Validator):
    """
    Validator to ensure a value is a string.
    """

    def validate(self, value: Any, name: str) -> None:
        if not isinstance(value, str):
            raise ValidationException(f'{name} must be a string.')


class IntegerValidator(Validator):
    """
    Validator to ensure a value is an integer.
    """

    def validate(self, value: Any, name: str) -> None:
        if not isinstance(value, int):
            raise ValidationException(f'{name} must be an integer.')


class MaxValueValidator(Validator):
    """
    Validator to ensure a value does not exceed a maximum.
    """

    def __init__(self, max_value: int) -> None:
        self.max_value = max_value

    def validate(self, value: int, name: str) -> None:
        if value > self.max_value:
            raise ValidationException(f'{name} must not be greater than {self.max_value}.')


class MinValueValidator(Validator):
    """
    Validator to ensure a value is not below a minimum.
    """

    def __init__(self, min_value: int) -> None:
        self.min_value = min_value

    def validate(self, value: int, name: str) -> None:
        if value < self.min_value:
            raise ValidationException(f'{name} must not be less than {self.min_value}.')


class MinLengthValidator(Validator):
    """
    Validator to ensure the length of a value is not below a minimum.
    """

    def __init__(self, min_length: int) -> None:
        self.min_length = min_length

    def validate(self, value: str, name: str) -> None:
        if len(value) < self.min_length:
            raise ValidationException(f'{name} must not be shorter than {self.min_length} characters.')


class MaxLengthValidator(Validator):
    """
    Validator to ensure the length of a value does not exceed a maximum.
    """

    def __init__(self, max_length: int) -> None:
        self.max_length = max_length

    def validate(self, value: str, name: str) -> None:
        if len(value) > self.max_length:
            raise ValidationException(f'{name} must not be longer than {self.max_length} characters.')


class DateValidator(Validator):

    def validate(self, value, key=None):
        if not value:
            return
        if value and isinstance(value, str):
            try:
                value = datetime.date(*time.strptime(value, '%Y-%m-%d')[:3])
            except ValueError:
                pass
        if value and not isinstance(value, datetime.date):
            raise ValidationException(
                '{0}: This value should be a valid date object.'.format(key))


class DateTimeValidator(Validator):

    def validate(self, value, key=None):
        if not value:
            return
        if value and isinstance(value, str):
            try:
                value = value.split('.', 1)[0]  # strip out microseconds
                value = value[0:19]  # remove timezone
                value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            except (IndexError, KeyError, ValueError):
                pass
        if value and not isinstance(value, datetime.datetime):
            raise ValidationException(
                '{0}: This value should be a valid datetime object.'.format(key))
class BooleanValidator(Validator):
    """
    Validator to ensure a value is a boolean.
    """

    def validate(self, value: bool, name: str) -> None:
        if not isinstance(value, bool):
            raise ValidationException(f'{name} must be a boolean.')


class ChoiceValidator(Validator):
    """
    Validator to ensure a value is within a set of choices.
    """

    def __init__(self, choices: List[Any]) -> None:
        self.choices = choices

    def validate(self, value: Any, name: str) -> None:
        if value not in self.choices:
            raise ValidationException(f'{name} must be one of {self.choices}.')


class DictValidator(Validator):
    """
    Validator to ensure a value is a dictionary.
    """

    def validate(self, value: Dict[Any, Any], name: str) -> None:
        if not isinstance(value, dict):
            raise ValidationException(f'{name} must be a dictionary.')


class ListValidator(Validator):
    """
    Validator to ensure a value is a list.
    """

    def validate(self, value: List[Any], name: str) -> None:
        if not isinstance(value, list):
            raise ValidationException(f'{name} must be a list.')


class ForeignValidator(Validator):
    """
    Validator for foreign key relationships.
    """

    def __init__(self, foreign_class: Any) -> None:
        self.foreign_class = foreign_class

    def validate(self, value: Any, name: str) -> None:
        if not isinstance(value, self.foreign_class):
            raise ValidationException(f'{name} must be an instance of {self.foreign_class.__name__}.')


class MultiValidator(Validator):
    """
    Validator that allows combining multiple validators.
    """

    def __init__(self, validators: List[Validator]) -> None:
        self.validators = validators

    def validate(self, value: Any, name: str) -> None:
        for validator in self.validators:
            validator.validate(value, name)


class FloatValidator(Validator):
    """
    Validator to ensure a value is a float.
    """

    def validate(self, value: Any, name: str) -> None:
        """
        Validates that the given value is a float.

        Args:
            value (Any): The value to validate.
            name (str): The name of the property being validated.

        Raises:
            ValidationException: If the value is not a float.
        """
        if not isinstance(value, float):
            raise ValidationException(f'{name} must be a float.')


class SlugValidator(Validator):
    """
    Validator to ensure a value is a valid slug.
    """

    def __init__(self):
        self.slug_pattern = re.compile(r'^[-a-zA-Z0-9_]+$')

    def validate(self, value: str, name: str) -> None:
        """
        Validates that the given value is a valid slug.

        Args:
            value (str): The value to validate.
            name (str): The name of the property being validated.

        Raises:
            ValidationException: If the value is not a valid slug.
        """
        if not isinstance(value, str) or not self.slug_pattern.match(value):
            raise ValidationException(f'{name} must be a valid slug (only letters, numbers, hyphens, and underscores).')


class EmailValidator(Validator):
    """
    Validator to ensure a value is a valid email address.
    """

    def __init__(self):
        self.email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

    def validate(self, value: str, name: str) -> None:
        """
        Validates that the given value is a valid email address.

        Args:
            value (str): The value to validate.
            name (str): The name of the property being validated.

        Raises:
            ValidationException: If the value is not a valid email address.
        """
        if not isinstance(value, str) or not self.email_pattern.match(value):
            raise ValidationException(f'{name} must be a valid email address.')

class ForeignListValidator(Validator):
    """
    Validator to ensure all items in a list are instances of a specified class.
    """

    def __init__(self, foreign_class: Type[Any]) -> None:
        """
        Initializes the ForeignListValidator with a specified class.

        Args:
            foreign_class (Type[Any]): The class that all list items should be instances of.
        """
        self.foreign_class = foreign_class

    def validate(self, value: List[Any], name: str) -> None:
        """
        Validates that all items in the list are instances of the specified class.

        Args:
            value (List[Any]): The list to validate.
            name (str): The name of the property being validated.

        Raises:
            ValidationException: If any item in the list is not an instance of the specified class.
        """
        if not all(isinstance(item, self.foreign_class) for item in value):
            raise ValidationException(f'All items in {name} must be instances of {self.foreign_class.__name__}.')



