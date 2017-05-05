from ..declarative import DeclaredVars as DV, \
    DeclarativeVariablesMetaclass as DVM
from ..schema import BaseSchema
from ..properties import BaseProperty


class DeclaredVars(DV):
    base_field_class = BaseProperty
    base_field_type = '_base_properties'


class DeclarativeVariablesMetaclass(DVM):
    declared_vars_class = DeclaredVars


class Schema(BaseSchema,metaclass=DeclarativeVariablesMetaclass):

    BUILTIN_DOC_ATTRS = []