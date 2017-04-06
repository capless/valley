import collections
import datetime
import json
import six
import time

from valley.exceptions import ValidationException
from .validators import (RequiredValidator, StringValidator,
                         MaxLengthValidator, MinLengthValidator,
                         IntegerValidator, MaxValueValidator,
                         MinValueValidator, FloatValidator,
                         DateValidator, DateTimeValidator, BooleanValidator,
                         SlugValidator, EmailValidator,DictValidator,
                         ChoiceValidator,ListValidator)


class VariableMixin(object):

    def get_validators(self):
        if self.required:
            self.validators.insert(0, RequiredValidator())
        if self.choices:
            self.validators.insert(0, ChoiceValidator(self.choices))

    def validate(self, value, key):
        if not value and not isinstance(self.get_default_value(), type(None)):
            value = self.get_default_value()
        for i in self.validators:
            i.validate(value, key)

    def get_default_value(self):
        """ return default value """
        default = self.default_value
        if isinstance(default, collections.Callable):
            default = default()
        return default

    def get_db_value(self, value):
        return value

    def get_python_value(self, value):
        return value


class CharVariableMixin(VariableMixin):

    def get_validators(self):
        super(CharVariableMixin, self).get_validators()
        self.validators.append(StringValidator())
        if self.kwargs.get('min_length'):
            self.validators.append(MinLengthValidator(
                self.kwargs.get('min_length')))

        if self.kwargs.get('max_length'):
            self.validators.append(MaxLengthValidator(
                self.kwargs.get('max_length')))

    def get_db_value(self, value):
        return str(value)

    def get_python_value(self, value):
        if not value:
            return None
        return str(value)

class SlugVariableMixin(CharVariableMixin):

    def get_validators(self):
        super(SlugVariableMixin, self).get_validators()
        self.validators.append(SlugValidator())


class EmailVariableMixin(CharVariableMixin):

    def get_validators(self):
        super(EmailVariableMixin, self).get_validators()
        self.validators.append(EmailValidator())


class NumericVariableMixin(VariableMixin):

    def get_validators(self):
        super(NumericVariableMixin, self).get_validators()

        if self.kwargs.get('max_value'):
            self.validators.append(MaxValueValidator(
                self.kwargs.get('max_value')))

        if self.kwargs.get('min_value'):
            self.validators.append(MinValueValidator(
                self.kwargs.get('min_value')))


class IntegerVariableMixin(NumericVariableMixin):

    def get_validators(self):
        super(IntegerVariableMixin, self).get_validators()
        self.validators.insert(0, IntegerValidator())

    def get_db_value(self, value):
        return int(value)

    def get_python_value(self, value):
        if not value:
            return None
        return int(value)


class FloatVariableMixin(NumericVariableMixin):

    def get_validators(self):
        super(FloatVariableMixin, self).get_validators()
        self.validators.insert(0, FloatValidator())

    def get_db_value(self, value):
        return float(value)

    def get_python_value(self, value):
        if not value:
            return None
        return float(value)


class DateMixin(VariableMixin):

    def get_validators(self):
        super(DateMixin, self).get_validators()
        self.validators.insert(0, DateValidator())

    def now(self):
        return datetime.datetime.now().date()

    def get_default_value(self):
        default = self.default_value
        if self.auto_now or self.auto_now_add:
            return self.now()
        return default

    def get_python_value(self, value):
        if not value:
            return None
        if isinstance(value, six.string_types):
            try:
                value = datetime.date(*time.strptime(value, '%Y-%m-%d')[:3])
            except ValueError as e:
                raise ValueError('Invalid ISO date %r [%s]' % (value,
                                                               str(e)))
        return value

    def get_db_value(self, value):
        if value is None:
            return value
        return value.isoformat()


class DateTimeMixin(VariableMixin):

    def get_validators(self):
        super(DateTimeMixin, self).get_validators()
        self.validators.insert(0, DateTimeValidator())

    def get_default_value(self):
        default = self.default_value
        if self.auto_now or self.auto_now_add:
            return self.now()
        return default

    def get_python_value(self, value):
        if isinstance(value, six.string_types):
            try:
                value = value.split('.', 1)[0]  # strip out microseconds
                value = value[0:19]  # remove timezone
                value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            except ValueError as e:
                raise ValueError('Invalid ISO date/time %r [%s]' %
                                 (value, str(e)))
        return value

    def get_db_value(self, value):
        if not value:
            return None
        if self.auto_now:
            value = self.now()

        if value is None:
            return value

        return value.replace(microsecond=0).isoformat() + 'Z'

    def now(self):
        return datetime.datetime.utcnow()


class BooleanMixin(VariableMixin):

    def get_validators(self):
        self.validators = [BooleanValidator()]

    def get_db_value(self, value):
        return bool(value)

    def get_python_value(self, value):
        if not value:
            return False
        try:
            BooleanValidator().validate(value, 'boolean')
        except ValidationException:
            return value
        return bool(value)


class DictMixin(VariableMixin):

    def get_validators(self):
        super(DictMixin, self).get_validators()
        self.validators.insert(0, DictValidator())

    def get_db_value(self, value):
        return json.dumps(value)

    def get_python_value(self, value):
        try:
            return json.loads(value)
        except TypeError:
            return dict(value)


class ListMixin(VariableMixin):

    def get_validators(self):
        super(ListMixin, self).get_validators()
        self.validators.insert(0, DictValidator())

    def get_db_value(self, value):
        return json.dumps(value)

    def get_python_value(self, value):
        try:
            return json.loads(value)
        except TypeError:
            return list(value)