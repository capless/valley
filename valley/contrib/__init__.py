from six import with_metaclass

from valley.declarative import DeclaredVars as DV, \
    DeclarativeVariablesMetaclass as DVM
from valley.schema import BaseSchema
from valley.properties import BaseProperty


class DeclaredVars(DV):
    base_field_class = BaseProperty
    base_field_type = '_base_properties'


class DeclarativeVariablesMetaclass(DVM):
    declared_vars_class = DeclaredVars


class Schema(with_metaclass(DeclarativeVariablesMetaclass, BaseSchema)):

    BUILTIN_DOC_ATTRS = []