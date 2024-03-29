import datetime
import unittest

from valley.validators import (RequiredValidator, DateTimeValidator,
                               DateValidator, FloatValidator, IntegerValidator,
                               MaxLengthValidator, MinLengthValidator,
                               MaxValueValidator, MinValueValidator,
                               StringValidator, ValidationException,
                               BooleanValidator, DictValidator,
                               ListValidator
                               )


class ValidatorsTestCase(unittest.TestCase):

    def test_required_validator(self):
        with self.assertRaises(ValidationException) as vm:
            RequiredValidator().validate(None, 'first_name')
        self.assertEqual(str(vm.exception),
                         'first_name is required and cannot be empty.')
        # Test with valid input
        RequiredValidator().validate('First Name', 'first_name')

    def test_datetime_validator(self):
        with self.assertRaises(ValidationException) as vm:
            DateTimeValidator().validate(datetime.date.today(), 'date_created')
        self.assertEqual(str(vm.exception),
                         'date_created: This value should be a valid datetime object.')
        # Test with valid input
        DateTimeValidator().validate(datetime.datetime.now(), 'date_created')

    def test_date_validator(self):
        with self.assertRaises(ValidationException) as vm:
            DateValidator().validate('not a date', 'date_created')
        self.assertEqual(str(vm.exception),
                         'date_created: This value should be a valid date object.')
        # Test with valid input
        DateValidator().validate(datetime.date.today(), 'date_created')

    def test_float_validator(self):
        with self.assertRaises(ValidationException) as vm:
            FloatValidator().validate(1, 'no_packages')
        self.assertEqual(str(vm.exception),
                         'no_packages must be a float.')
        # Test with valid input
        FloatValidator().validate(1.3, 'no_packages')

    def test_integer_validator(self):
        with self.assertRaises(ValidationException) as vm:
            IntegerValidator().validate(1.2, 'no_packages')
        self.assertEqual(str(vm.exception),
                         'no_packages must be an integer.')
        # Test with valid input
        IntegerValidator().validate(1, 'no_packages')

    def test_max_length_validator(self):
        with self.assertRaises(ValidationException) as vm:
            MaxLengthValidator(2).validate('123', 'no_packages')
        self.assertEqual(str(vm.exception),
                         'no_packages must not be longer than 2 characters.')
        # Test with valid input
        MaxLengthValidator(2).validate('12', 'no_packages')

    def test_min_length_validator(self):
        with self.assertRaises(ValidationException) as vm:
            MinLengthValidator(2).validate('1', 'no_packages')
        self.assertEqual(str(vm.exception),
                         'no_packages must not be shorter than 2 characters.')
        # Test with valid input
        MinLengthValidator(2).validate('123', 'no_packages')

    def test_max_value_validator(self):
        with self.assertRaises(ValidationException) as vm:
            MaxValueValidator(2).validate(3, 'no_packages')
        self.assertEqual(str(vm.exception),
                         'no_packages must not be greater than 2.')
        # Test with valid input
        MaxValueValidator(2).validate(1, 'no_packages')

    def test_min_value_validator(self):
        with self.assertRaises(ValidationException) as vm:
            MinValueValidator(2).validate(1, 'no_packages')
        self.assertEqual(str(vm.exception),
                         'no_packages must not be less than 2.')
        # Test with valid input
        MinValueValidator(2).validate(3, 'no_packages')

    def test_string_validator(self):
        with self.assertRaises(ValidationException) as vm:
            StringValidator().validate(1, 'last_name')
        self.assertEqual(str(vm.exception),
                         'last_name must be a string.')
        # Test with valid input
        StringValidator().validate('Jones', 'last_name')

    def test_boolean_validator(self):
        with self.assertRaises(ValidationException) as vm:
            BooleanValidator().validate(1, 'last_name')
        self.assertEqual(str(vm.exception),
                         'last_name must be a boolean.')
        # Test with valid input
        BooleanValidator().validate(True, 'last_name')
        BooleanValidator().validate(False, 'last_name')

    def test_dict_validator(self):
        with self.assertRaises(ValidationException) as vm:
            DictValidator().validate(1, 'person')
        self.assertEqual(str(vm.exception),
                         'person must be a dictionary.')
        # Test with valid input
        DictValidator().validate({'first': 'Brian', 'last': 'Jones'}, 'person')

    def test_list_validator(self):
        with self.assertRaises(ValidationException) as vm:
            ListValidator().validate(1, 'schools')
        self.assertEqual(str(vm.exception),
                         'schools must be a list.')
        # Test with valid input
        ListValidator().validate(['Ridge Valley High', 'Lewis Cone Elementary'], 'schools')


if __name__ == '__main__':
    unittest.main()
