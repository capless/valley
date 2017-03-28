import collections

from valley.mixins import VariableMixin


class BaseProperty(VariableMixin, object):

    def __init__(
        self,
        default_value=None,
        required=False,
        validators=[],
        verbose_name=None,
        **kwargs
    ):
        self.default_value = default_value
        self.required = required
        self.kwargs = kwargs
        self.validators = list()
        self.get_validators()
        self.validators = set(self.validators)
        if verbose_name:
            self.verbose_name = verbose_name

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


class CharProperty(CharVariableMixin, BaseProperty):

    def get_db_value(self, value):
        return str(value)

    def get_python_value(self, value):
        if not value:
            return None
        return str(value)


class IntegerProperty(IntegerVariableMixin, BaseProperty):

    def get_db_value(self, value):
        return int(value)

    def get_python_value(self, value):
        if not value:
            return None
        return int(value)


class FloatProperty(FloatVariableMixin, BaseProperty):

    def get_db_value(self, value):
        return float(value)

    def get_python_value(self, value):
        if not value:
            return None
        return float(value)


class BooleanProperty(BooleanMixin, BaseProperty):

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


class DateProperty(DateMixin, BaseProperty):

    def __init__(
            self,
            default_value=None,
            required=True,
            validators=[],
            verbose_name=None,
            auto_now=False,
            auto_now_add=False,
            **kwargs):

        super(
            DateProperty,
            self).__init__(
            default_value=default_value,
            required=required,
            validators=validators,
            verbose_name=verbose_name,
            **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

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


class DateTimeProperty(DateTimeMixin, BaseProperty):

    def __init__(
            self,
            default_value=None,
            required=True,
            validators=[],
            verbose_name=None,
            auto_now=False,
            auto_now_add=False,
            **kwargs):

        super(
            DateTimeProperty,
            self).__init__(
            default_value=default_value,
            required=required,
            validators=validators,
            verbose_name=verbose_name,
            **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

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
