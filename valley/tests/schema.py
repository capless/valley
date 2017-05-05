import unittest


from valley.contrib import Schema
from valley.exceptions import ValidationException
from valley.properties import CharProperty, EmailProperty, SlugProperty, \
    IntegerProperty, FloatProperty, DateProperty, \
    DateTimeProperty


class Student(Schema):
    _create_error_dict = True
    name = CharProperty(required=True,min_length=5,max_length=20)
    slug = SlugProperty(required=True,min_length=5,max_length=25)
    email = EmailProperty(required=True)
    age = IntegerProperty(min_value=5,max_value=18)
    gpa = FloatProperty(min_value=0,max_value=4.5)
    date = DateProperty(required=False)
    datetime = DateTimeProperty(required=False)


class StudentB(Student):
    _create_error_dict = False


class SchemaTestCase(unittest.TestCase):

    def setUp(self):
        self.student = Student(name='Frank White',slug='frank-white',
                    email='frank@white.com',age=18,
                    gpa=3.0,date='2017-01-10',
                    datetime='2017-01-10T12:00:00'
                    )

    def test_valid(self):
        self.student.validate()

    def test_long_name(self):
        self.student.name = 'Frank Lindsay Hightower III'
        self.student.validate()
        ed = {'name': 'name: This value should have a length lesser than 20. '
                      'Currently Frank Lindsay Hightower III'}
        self.assertDictEqual(ed, self.student._errors)

    def test_short_name(self):
        self.student.name = 'Ira'
        self.student.validate()
        ed = {'name': 'name: This value should have a length greater '
                      'than 5. Currently Ira'}
        self.assertDictEqual(ed,self.student._errors)

    def test_no_name(self):
        self.student.name = None
        self.student.validate()
        ed = {'name': 'name: This value is required'}
        self.assertDictEqual(ed, self.student._errors)

    def test_slug_space(self):
        self.student.slug = 'Some City'
        self.student.validate()
        ed = {'slug': 'slug: This value should be a slug. ex. pooter-is-awesome'}
        self.assertDictEqual(ed, self.student._errors)

    def test_email_space(self):
        self.student.email = 'Some City'
        self.student.validate()
        ed = {'email': 'email: This value should be a valid email address'}
        self.assertDictEqual(ed, self.student._errors)

    def test_email_wrong(self):
        self.student.email = 'e+ e@g.com'
        self.student.validate()
        ed = {'email': 'email: This value should be a valid email address'}
        self.assertDictEqual(ed, self.student._errors)

    def test_age_numeric_string(self):
        self.student.age = '5'
        self.student.validate()
        ed = {'age': 'age: This value should be an integer'}
        self.assertEqual(ed, self.student._errors)

    def test_age_numeric_float(self):
        self.student.age = 5.0
        self.student.validate()
        ed = {'age': 'age: This value should be an integer'}
        self.assertDictEqual(ed, self.student._errors)


class SchemaMethods(unittest.TestCase):

    def setUp(self):
        attr_dict = {
            'name':'Frank White',
            'slug':'frank-white',
            'email':'frank@white.com',
            'age':18, 'gpa':3.0,
            'date':'2017-01-10',
            'datetime':'2017-01-10T12:00:00'
        }
        self.student = Student(**attr_dict)
        self.studentb = StudentB(**attr_dict)

    def test_setattr(self):
        self.student.name = 'Curious George'
        self.assertEqual(self.student._data.get('name'),'Curious George')

    def test_getattr(self):
        self.assertEqual(self.student.name,'Frank White')

    def test_process_doc_kwargs(self):
        response = self.student.process_schema_kwargs({'name':1,'slug':1})
        self.assertEqual(response,{'name':'1','slug':'1','email':None,
                                   'age':None,'gpa':None,'date':None,
                                   'datetime':None})

    def test_error_dict_false_validate(self):
        self.studentb.name = 1
        self.assertRaises(ValidationException,self.studentb.validate)

