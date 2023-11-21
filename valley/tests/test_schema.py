import unittest

from valley.exceptions import ValidationException
from valley.tests.examples.example_schemas import StudentB, Student, Troop, bruno, blitz, cocker


class SchemaTestCase(unittest.TestCase):

    def setUp(self):
        self.student = Student(name='Frank White', slug='frank-white',
                               email='frank@white.com', age=18,
                               gpa=3.0, date='2017-01-10',
                               datetime='2017-01-10T12:00:00', active=False
                               )
        self.troop = Troop(name='Durham', dogs=[bruno, blitz],
                           primary_breed=cocker)

    def test_valid(self):
        self.student.validate()
        self.assertEqual(True, self.student._is_valid)
        self.assertDictEqual(self.student._errors, {})

    def test_foreign_valid(self):
        self.troop.validate()
        self.assertEqual(True, self.troop._is_valid)
        self.assertDictEqual(self.troop._errors, {})

    def test_foreign_property_wrong_type(self):
        self.troop.primary_breed = 'Cocker'
        self.troop.validate()
        self.assertEqual(False, self.troop._is_valid)
        self.assertDictEqual({'primary_breed': 'primary_breed must be an instance of Breed.'},
                             self.troop._errors)

    def test_foreign_list_property_wrong_type(self):
        self.troop.dogs = ['Test', bruno, blitz]
        self.troop.validate()
        self.assertEqual(False, self.troop._is_valid)
        self.assertDictEqual({'dogs': 'All items in dogs must be instances of Dog.'},
                             self.troop._errors)

    def test_long_name(self):
        self.student.name = 'Frank Lindsay Hightower III'
        self.student.validate()
        self.assertEqual(False, self.student._is_valid)
        ed = {'name': 'name must not be longer than 20 characters.'}
        self.assertDictEqual(ed, self.student._errors)

    def test_short_name(self):
        self.student.name = 'Ira'
        self.student.validate()
        self.assertEqual(False, self.student._is_valid)
        ed = {'name': 'name must not be shorter than 5 characters.'}
        self.assertDictEqual(ed, self.student._errors)

    def test_no_name(self):
        self.student.name = None
        self.student.validate()
        self.assertEqual(False, self.student._is_valid)
        ed = {'name': 'name is required and cannot be empty.'}
        self.assertDictEqual(ed, self.student._errors)

    def test_slug_space(self):
        self.student.slug = 'Some City'
        self.student.validate()
        ed = {'slug': 'slug must be a valid slug (only letters, numbers, hyphens, and underscores).'}
        self.assertDictEqual(ed, self.student._errors)

    def test_email_space(self):
        self.student.email = 'Some City'
        self.student.validate()
        ed = {'email': 'email must be a valid email address.'}
        self.assertDictEqual(ed, self.student._errors)

    def test_email_wrong(self):
        self.student.email = 'e+ e@g.com'
        self.student.validate()
        ed = {'email': 'email must be a valid email address.'}
        self.assertDictEqual(ed, self.student._errors)

    def test_age_numeric_string(self):
        self.student.age = '5'
        self.student.validate()
        ed = {'age': 'age must be an integer.'}
        self.assertDictEqual(ed, self.student._errors)

    def test_age_numeric_float(self):
        self.student.age = 5.0
        self.student.validate()
        ed = {'age': 'age must be an integer.'}
        self.assertDictEqual(ed, self.student._errors)


class SchemaMethods(unittest.TestCase):

    def setUp(self):
        attr_dict = {
            'name': 'Frank White',
            'slug': 'frank-white',
            'email': 'frank@white.com',
            'age': 18, 'gpa': 3.0,
            'date': '2017-01-10',
            'datetime': '2017-01-10T12:00:00'
        }
        self.student = Student(**attr_dict)
        self.studentb = StudentB(**attr_dict)

    def test_setattr(self):
        self.student.name = 'Curious George'
        self.assertEqual(self.student._data.get('name'), 'Curious George')

    def test_getattr(self):
        self.assertEqual(self.student.name, 'Frank White')

    def test_error_dict_false_validate(self):
        self.studentb.name = 1
        self.assertRaises(ValidationException, self.studentb.validate)


if __name__ == '__main__':
    unittest.main()
