import datetime
import re
import time


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
    "BooleanValidator",
    "ChoiceValidator",
    "DictValidator",
    "ListValidator"
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
        if value and not isinstance(value, str):
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
                'have a value lesser than or equal to '
                '{1}. Currently {2}'.format(key, self.compare_value, value)
            )


class MinValueValidator(MaxValueValidator):

    def validate(self, value, key=None):
        if not value:
            return
        if isinstance(value, (float, int)) and value < self.compare_value:
            raise ValidationException(
                '{0}: This value should '
                'have a value greater than or equal to '
                '{1}. Currently {2}'.format(key, self.compare_value, value)
            )


class MaxLengthValidator(Validator):

    def __init__(self, length):
        self.length = length

    def validate(self, value, key=None):
        if not value:
            return
        try:
            if not isinstance(value, int) and len(value) > self.length:
                raise ValidationException(
                    '{0}: This value should '
                    'have a length lesser than or equal to '
                    '{1}. Currently {2}'.format(key, self.length, value)
                )
        except TypeError:
            raise ValidationException(
                '{0}: This value should '
                'have a length lesser than or equal to '
                '{1}. Currently unknown'.format(key, self.length)
            )


class MinLengthValidator(MaxLengthValidator):

    def validate(self, value, key):
        if not value:
            return
        try:
            if not isinstance(value, int) and len(value) < self.length:
                raise ValidationException(
                    '{0}: This value should '
                    'have a length greater than or equal to '
                    '{1}. Currently {2}'.format(key, self.length, value)
                )
        except TypeError:
            raise ValidationException(
                '{0}: This value should '
                'have a length greater than or equal to'
                '{1}. Currently unknown'.format(key, self.length)
            )


class BooleanValidator(Validator):

    def validate(self, value, key):
        if not isinstance(value, bool):
            raise ValidationException(
                '{0}: This value should be True or False.'.format(key)
            )


class ChoiceValidator(Validator):

    def __init__(self,choices):
        self.choices = choices

    def validate(self, value, key):
        if value:
            if not value in self.choices.values():
                raise ValidationException(
                    '{0}: This value is outside '
                    'of the specified choices.'.format(key)
                )


class DictValidator(Validator):

    def validate(self, value, key):
        if value:
            if not isinstance(value,dict):
                raise ValidationException(
                    '{0}: This value should be a dict object.'.format(key)
                )


class ListValidator(Validator):

    def validate(self, value, key):
        if value:
            if not isinstance(value,list):
                raise ValidationException(
                    '{0}: This value should be a list object.'.format(key)
                )

class ForeignValidator(Validator):

    def __init__(self, foreign_class):
        self.foreign_class = foreign_class

    def validate(self, value, key):
        if value:
            if not isinstance(value,self.foreign_class):
                raise ValidationException('{0}: This value ({1}) should be an instance of {2}.'.format(
                    key, value, self.foreign_class.__name__))


class ForeignListValidator(ForeignValidator):

    def validate(self, value, key):
        if value:
            for obj in value:
                if not isinstance(obj,self.foreign_class):
                    raise ValidationException(
                        '{0}: This value ({1}) should be an instance of {2}.'.format(
                            key, obj, self.foreign_class.__name__)
                    )

