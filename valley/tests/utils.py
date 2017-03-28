import unittest
from valley.utils import import_util,import_mod


class UtilTest(unittest.TestCase):

    def test_import_util(self):
        klass = import_util('valley.mixins.VariableMixin')
        self.assertEqual('VariableMixin', klass.__name__)

    def test_import_mod(self):
        mod = import_mod('valley.mixins')
        self.assertTrue(hasattr(mod, 'VariableMixin'))
