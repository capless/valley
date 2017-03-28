import datetime
import re
import time
import six

from .exceptions import ValidationException

__all__ = [
    "Validator",
    "RequiredValidator",
    "StringValidator",
    "IntegerValidator",
    "MaxValueValidator",
    "MinValueValidator",
    "MinLengthValidator",
    "MaxLengthValidator",
    "DateValidator",
    "DateTimeValidator",
]

#Credit to the Django project
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain


slug_re = re.compile(r'^[-\w]+$')


class Validator(object):

    def validate(self, value, key):
        raise NotImplementedError


class RequiredValidator(Validator):

    def validate(self, value, key):
        if not value:
            raise ValidationException(
                '{0}: This value is required'.format(key)
            )


class StringValidator(Validator):

    def validate(self, value, key=None):
        if not value:
            return
        if value and not isinstance(value, six.string_types):
            raise ValidationException(
                '{0}: This value should '
                'be a string'.format(key)
            )


class SlugValidator(Validator):

    error_msg = '{0}: This value should be a slug. ex. pooter-is-awesome'

    def validate(self, value, key):
        if not value:
            return
        try:
            if not slug_re.match(value):
                raise ValidationException(self.error_msg.format(key))
        except TypeError:
            raise ValidationException(self.error_msg.format(key))


class EmailValidator(Validator):
    error_msg = '{0}: This value should be a valid email address'

    def validate(self, value, key):
        if not value:
            return
        try:
            if not email_re.match(value):
                raise ValidationException(self.error_msg.format(key))
        except TypeError:
            raise ValidationException(self.error_msg.format(key))


class DateValidator(Validator):

    def validate(self, value, key=None):
        if not value:
            return
        if value and isinstance(value, six.string_types):
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
        if value and isinstance(value, six.string_types):
            try:
                value = value.split('.', 1)[0]  # strip out microseconds
                value = value[0:19]  # remove timezone
                value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            except (IndexError, KeyError, ValueError):
                pass
        if value and not isinstance(value, datetime.datetime):
            raise ValidationException(
                '{0}: This value should be a valid datetime object.'.format(key))


class IntegerValidator(Validator):

    def validate(self, value, key=None):
        if not value:
            return
        if value and not isinstance(value, int):
            raise ValidationException(
                '{0}: This value should be an integer'.format(key))


class FloatValidator(Validator):

    def validate(self, value, key=None):
        if not value:
            return
        if value and not isinstance(value, float):
            raise ValidationException(
                '{0}: This value should be a float.'.format(key))


class MaxValueValidator(Validator):

    def __init__(self, compare_value):
        self.compare_value = compare_value

    def validate(self, value, key=None):
        if not value:
            return
        if isinstance(value, (float, int)) and value > self.compare_value:
            raise ValidationException(
                '{0}: This value should '
                'have a value lesser than '
                '{1}. Currently {2}'.format(key, self.compare_value, value)
            )


class MinValueValidator(MaxValueValidator):

    def validate(self, value, key=None):
        if not value:
            return
        if isinstance(value, (float, int)) and value < self.compare_value:
            raise ValidationException(
                '{0}: This value should '
                'have a value greater than '
                '{1}. Currently {2}'.format(key, self.compare_value, value)
            )


class MaxLengthValidator(Validator):

    def __init__(self, length):
        self.length = length

    def validate(self, value, key=None):
        if not value:
            return
        if not isinstance(value, int) and len(value) > self.length:
            raise ValidationException(
                '{0}: This value should '
                'have a length lesser than '
                '{1}. Currently {2}'.format(key, self.length, value)
            )


class MinLengthValidator(MaxLengthValidator):

    def validate(self, value, key):
        if not value:
            return
        if not isinstance(value, int) and len(value) < self.length:
            raise ValidationException(
                '{0}: This value should '
                'have a length greater than '
                '{1}. Currently {2}'.format(key, self.length, value)
            )


class BooleanValidator(Validator):

    def validate(self, value, key):
        try:
            int(value)
        except (TypeError, ValueError):
            raise ValidationException(
                '{0}: This value should be True or False.'.format(key)
            )
        if not isinstance(value, bool):
            raise ValidationException(
                '{0}: This value should be True or False.'.format(key)
            )
