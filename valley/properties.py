from valley.mixins import VariableMixin, CharVariableMixin, \
    IntegerVariableMixin, FloatVariableMixin, BooleanMixin, \
    DateMixin, DateTimeMixin, SlugVariableMixin, EmailVariableMixin



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


class OrderedBaseProperty(BaseProperty):
    _creation_counter = 0

    def __init__(
            self,
            default_value=None,
            required=False,
            validators=[],
            verbose_name=None,
            **kwargs
    ):
        super(OrderedBaseProperty, self).__init__(default_value=default_value,
                                                  required=required,
                                                  validators=validators,
                                                  verbose_name=verbose_name,
                                                  **kwargs)
        self._creation_counter = OrderedBaseProperty._creation_counter
        OrderedBaseProperty._creation_counter += 1


class CharProperty(CharVariableMixin, BaseProperty):
    pass


class SlugProperty(SlugVariableMixin, CharProperty):
    pass


class EmailProperty(EmailVariableMixin, CharProperty):
    pass


class IntegerProperty(IntegerVariableMixin, BaseProperty):
    pass


class FloatProperty(FloatVariableMixin, BaseProperty):
    pass


class BooleanProperty(BooleanMixin, BaseProperty):
    pass


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

