class DeclaredVars(object):

    base_field_class = None

    def get_declared_variables(self,bases, attrs):
        properties = {}
        f_update = properties.update
        attrs_pop = attrs.pop
        for variable_name, obj in list(attrs.items()):
            if isinstance(obj, self.base_field_class):
                f_update({variable_name: attrs_pop(variable_name)})

        for base in bases:
            if hasattr(base, '_base_properties'):
                bft = base._base_properties
                if len(bft) > 0:
                    f_update(bft)
        return properties


class DeclarativeVariablesMetaclass(type):
    """
    Partially ripped off from Django's forms.
    http://code.djangoproject.com/browser/django/trunk/django/forms/forms.py
    """

    declared_vars_class = None

    def __new__(cls, name, bases, attrs):
        attrs['_base_properties'] = cls.declared_vars_class().get_declared_variables(bases, attrs)
        new_class = super(DeclarativeVariablesMetaclass,
                          cls).__new__(cls, name, bases, attrs)

        return new_class