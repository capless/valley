import logging

from valley.mixins import VariableMixin, CharVariableMixin, \
    IntegerVariableMixin, FloatVariableMixin, BooleanMixin, \
    DateMixin, DateTimeMixin, SlugVariableMixin, EmailVariableMixin, \
    DictMixin, ListMixin, ForeignMixin, ForeignListMixin, MultiMixin


LOGGER = logging.getLogger('valley')


class BaseProperty(VariableMixin, object):
    default_value = None
    allow_required = True
    def __init__(
        self,
        default_value=None,
        required=False,
        validators=[],
        choices=None,
        verbose_name=None,
        **kwargs
    ):
        self.default_value = default_value or self.default_value
        if self.allow_required == True:
            self.required = required
        else:
            self.required = False
            if required == True:
                LOGGER.warning(
                    'The required argument has no effect on {}'.format(
                        self.__class__.__name__))
        self.choices = choices
        self.kwargs = kwargs
        if isinstance(validators,list):
            self.validators = list(set(validators))
        else:
            self.validators = []

        self.get_validators()
        self.validators = set(self.validators)

        if verbose_name:
            self.verbose_name = verbose_name


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
    default_value = False
    allow_required = False

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


class DictProperty(DictMixin, BaseProperty):
    pass


class ListProperty(ListMixin, BaseProperty):
    pass


class ForeignProperty(ForeignMixin, BaseProperty):

    def __init__(self,foreign_class,return_type=None,return_prop=None,**kwargs):
        self.foreign_class = foreign_class
        super(ForeignProperty, self).__init__(**kwargs)
        self.return_type = return_type
        self.return_prop = return_prop


class ForeignListProperty(ForeignListMixin, BaseProperty):

    def __init__(self,foreign_class,return_type=None,return_prop=None,**kwargs):
        self.foreign_class = foreign_class
        super(ForeignListProperty, self).__init__(**kwargs)
        self.return_type = return_type
        self.return_prop = return_prop


class MultiProperty(MultiMixin,BaseProperty):

    def validate(self, value, key):
        super(MultiProperty, self).validate(value,key)
