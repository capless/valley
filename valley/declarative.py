import collections

class DeclaredVars(object):

    base_field_class = None

    def get_base_fields(self,bases, attrs):
        properties = {}
        p_update = properties.update
        attrs_pop = attrs.pop
        for variable_name, obj in list(attrs.items()):
            if isinstance(obj, self.base_field_class):
                properties[variable_name] = attrs_pop(variable_name)

        for base in bases:
            if hasattr(base, '_base_properties'):
                bft = base._base_properties
                if len(bft) > 0:
                    p_update(bft)
        return properties


class DeclarativeVariablesMetaclass(type):

    declared_vars_class = None

    def __new__(cls, name, bases, attrs):
        attrs['_base_properties'] = cls.declared_vars_class().get_base_fields(bases, attrs)
        new_class = super(DeclarativeVariablesMetaclass,
                          cls).__new__(cls, name, bases, attrs)

        return new_class

    @classmethod
    def __prepare__(mcls, cls, bases):
        return collections.OrderedDict()