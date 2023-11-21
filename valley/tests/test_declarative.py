import collections
import unittest

from valley.schema import BaseSchema
from valley.declarative import DeclaredVars, DeclarativeVariablesMetaclass
from valley.properties import BaseProperty


class TestField(BaseProperty):
    pass

class TestDeclaredVars(DeclaredVars):
    base_field_class = TestField


class TestDeclarativeVariablesMetaclass(DeclarativeVariablesMetaclass):
    declared_vars_class = TestDeclaredVars


class TestClass(BaseSchema, metaclass=TestDeclarativeVariablesMetaclass):
    BUILTIN_DOC_ATTRS = []
    field1 = TestField()
    field2 = TestField()

class DeclarativeTests(unittest.TestCase):

    def test_declared_vars_base_fields(self):
        """Test if base fields are correctly identified and collected."""
        declared_vars = TestDeclaredVars()
        bases = (TestClass,)
        attrs = {'field1': TestField(1), 'field2': TestField(2), 'not_a_field': 3}
        base_fields = declared_vars.get_base_fields(bases, attrs)

        self.assertIn('field1', base_fields)
        self.assertIn('field2', base_fields)
        self.assertNotIn('not_a_field', base_fields)

    def test_metaclass_new_instance(self):
        """Test if the metaclass correctly creates a new class instance."""
        instance = TestClass()
        self.assertTrue(hasattr(instance, '_base_properties'))
        self.assertIn('field1', instance._base_properties)
        self.assertIn('field2', instance._base_properties)

    def test_metaclass_prepare_namespace(self):
        """Test if __prepare__ method of metaclass returns an OrderedDict."""
        namespace = DeclarativeVariablesMetaclass.__prepare__('Test', (object,))
        self.assertIsInstance(namespace, collections.OrderedDict)


if __name__ == '__main__':
    unittest.main()
