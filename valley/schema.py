import collections

from valley import ValidationException


class BaseSchema(object):
    """
    Base class for all Kev Documents classes.
    """
    is_valid = False
    create_error_dict = False

    def __init__(self, **kwargs):
        self._data = self.process_schema_kwargs(kwargs)

    def __repr__(self):
        return '<{class_name}: {uni} >'.format(
            class_name=self.__class__.__name__, uni=self.__unicode__())

    def __unicode__(self):
        return '({0} Object)'.format(self.__class__.__name__)

    def __getattr__(self, name):
        if name in list(self._base_properties.keys()):
            prop = self._base_properties[name]
            return prop.get_python_value(self._data.get(name))


    def process_schema_kwargs(self, kwargs):
        schema_obj = {}
        for key, prop in list(self._base_properties.items()):
            try:
                value = prop.get_python_value(kwargs.get(key) or prop.get_default_value())
            except ValueError:
                value = kwargs.get(key) or prop.get_default_value()

            schema_obj[key] = value
        for i in self.BUILTIN_DOC_ATTRS:
            if kwargs.get(i):
                schema_obj[i] = kwargs[i]
        return schema_obj

    def validate(self):
        data = self._data.copy()
        for key, prop in list(self._base_properties.items()):
            prop_validate = getattr(self, '{}_validate'.format(key))
            self._errors = dict()
            try:
                prop.validate(data.get(key), key)
                # This allows devs to specify additional validation for a property
                if isinstance(prop_validate, collections.Callable):
                    prop_validate(data.get(key))
            except ValidationException as e:
                if self.create_error_list:
                    self._errors[key] = e.error_msg
                else:
                    raise e
            value = prop.get_python_value(data.get(key))
            data[key] = value
        self.is_valid = True
        self.cleaned_data = data

    @classmethod
    def get_class_name(cls):
        return cls.__name__.lower()

