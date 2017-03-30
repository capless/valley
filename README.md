# Valley

Python extensible schema validations and declarative syntax helpers.

## Installation

`pip install valley`

## Getting Started

```python
class Animal(Schema):
    name = CharProperty(required=True)
    species = CharProperty(required=True)
    color = CharProperty(required=True)
    meal_type = CharProperty()
    age = IntegerProperty(required=True)
    
frog = Animal(name='Kermit',species='frog',color='green',meal='carnivore',age=1)
frog.validate()
```

- [Library Comparison](https://github.com/capless/valley/blob/master/notebooks/valley-vs-schema-vs-schematics.ipynb) - **Valley** vs **Schema** vs **Schematics**
- [Projects using Valley](#projects-using-valley)
- [Schema and Declarative Syntax Helpers](#schema-and-declarative-syntax-helpers)
- [Properties](#properties)



### Projects Using Valley

- [kev](https://github.com/capless/kev) - **K.E.V.** (Keys, Extra Stuff, and Values) is a Python ORM for key-value stores. Currently supported backends are Redis, S3, DynamoDB, and a S3/Redis hybrid backend.
- [formy](https://github.com/capless/formy) - **Formy** is a Python forms library with Jinja2 templates

### Schema and Declarative Syntax Helpers

The schema class **[(valley.contrib.Schema)](https://github.com/capless/valley/blob/master/valley/contrib/__init__.py)** provides the model for validating properties. Valley also includes utilities **[(valley.declarative)](https://github.com/capless/valley/blob/master/valley/declarative.py)** to make building declarative syntax validation libraries easier. See an example below. 
 
```python
from six import with_metaclass

from valley.declarative import DeclaredVars as DV, \
    DeclarativeVariablesMetaclass as DVM
from valley.schema import BaseSchema
from valley.properties import *


class DeclaredVars(DV):
    base_field_class = BaseProperty
    base_field_type = '_base_properties'


class DeclarativeVariablesMetaclass(DVM):
    declared_vars_class = DeclaredVars


class Schema(with_metaclass(DeclarativeVariablesMetaclass, BaseSchema)):

    BUILTIN_DOC_ATTRS = []
    
#If you just want to build upon an existing schema use valley.contrib.Schema

class Animal(Schema):
    name = CharProperty(required=True)
    species = CharProperty(required=True)
    color = CharProperty(required=True)
    meal_type = CharProperty()
    age = IntegerProperty(required=True)
```

```python  
>>bear = Animal(name="Yogi",species="bear",color="brown",meal_type="carnivore",age=5)
>>bear.is_valid
False
>>bear.validate()
>>bear.is_valid
True
>>frog = Animal(name="Kermit",species="frog",color="green",meal_type="carnivore")
>>frog.is_valid
False
>>frog.validate()

ValidationException                       Traceback (most recent call last)

      1 frog = Animal(name='Frog',color='Green',meal_type='carnivore')
      2 
      3 frog.validate()

/home/coder/workspace/valley/valley/schema.pyc in validate(self)
     55                     self._errors[key] = e.error_msg
     56                 else:
     57                     raise e
     58             value = prop.get_python_value(data.get(key))
     59             data[key] = value

ValidationException: age: This value is required
```

### Properties

#### BaseProperty

Base class that all of the following properties are subclassed from.

##### Default Validators

- RequiredValidator (if the required kwarg is set)

#### CharProperty

Validates that the input is a string type. More specifically it checks `six.string_types`

##### Example

```python
from valley.properties import CharProperty

first_name = CharProperty(required=True,min_length=1,max_length=20)
first_name.validate('Some string','First Name')
```

##### Default Validators

- Validators from BaseProperty
- StringValidator
- MinLengthValidator (if min_length kwarg is set)
- MaxLengthValidator (if max_length kwarg is set)

#### SlugProperty

Validates that the input is a string type but is also a slug (ex. this-is-a-slug). 

##### Example

```python
from valley.properties import SlugProperty

slug = SlugProperty(required=True,min_length=1,max_length=20)
slug.validate('some-slug','Slug')
```

##### Default Validators

- Validators from BaseProperty
- StringValidator
- MinLengthValidator (if min_length kwarg is set)
- MaxLengthValidator (if max_length kwarg is set)
- SlugValidator

#### EmailProperty

Validates that the input is a string type but is also in valid email format. 

##### Example

```python
from valley.properties import EmailProperty

email = EmailProperty(required=True,min_length=1,max_length=20)
email.validate('you@you.com','Email')
```

##### Default Validators

- Validators from BaseProperty
- StringValidator
- MinLengthValidator (if min_length kwarg is set)
- MaxLengthValidator (if max_length kwarg is set)
- EmailValidator


#### IntegerProperty

Validates that the input is a integer type.

##### Example

```python
from valley.properties import IntegerProperty

age = IntegerProperty(required=True,min_value=1,max_value=20)
age.validate(5,'Age')
```

##### Default Validators

- Validators from BaseProperty
- IntegerValidator
- MinValuehValidator (if min_value kwarg is set)
- MaxLengthValidator (if max_value kwarg is set)


#### FloatProperty

Validates that the input is a float type.

##### Example

```python
from valley.properties import FloatProperty

gpa = FloatProperty(required=True,min_value=1,max_value=20)
gpa.validate(4.0,'GPA')
```

##### Default Validators

- Validators from BaseProperty
- FloatValidator
- MinValuehValidator (if min_value kwarg is set)
- MaxLengthValidator (if max_value kwarg is set)

#### BooleanProperty

Validataes that the input is a bool type.

##### Example

```python
from valley.properties import BooleanProperty

active = BooleanProperty()
active.validate(True,'Active')
```
##### Default Validators

- Validators from BaseProperty
- BooleanValidator

#### DateProperty

Validates that the input is a date object or a string that can be transformed to a date object.
 
##### Example

```python
from valley.properties import DateProperty

active = DateProperty(required=True)
active.validate('2017-03-27','Active')
```

##### Default Validators

- Validators from BaseProperty
- DateValidator


#### DateTimeProperty

Validates that the input is a datetime object or a string that can be transformed to a datetime object.

##### Example

```python
from valley.properties import DateTimeProperty

active = DateTimeProperty(required=True)
active.validate('2017-03-03 12:00:00','Active')
```

##### Default Validators

- Validators from BaseProperty
- DateTimeValidator

