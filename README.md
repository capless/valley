# valley

Python validation library.

- [Schema](#schema)
- [Properties](#properties)
- [Validators](#validators)
- [Declarative Syntax Helpers](#declarative-syntax-helpers)
- [Mixins](#mixins)
- [Utils](#utils)
- [Exceptions](#exceptions)

## Schema

Utility to make building declarative syntax validation libraries easier. 
 
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
<ipython-input-8-401f014a1e5c> in <module>()
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

## Properties

## Mixins

## Utils

## Exceptions