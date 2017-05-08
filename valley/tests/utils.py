import unittest
from valley.utils import import_util


class UtilTest(unittest.TestCase):

    def test_import_util(self):
        klass = import_util('valley.mixins.VariableMixin')
        self.assertEqual('VariableMixin', klass.__name__)