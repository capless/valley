![alt text](https://s3.amazonaws.com/capless/images/valley-small.png "Valley - Extensible Schema Validations and Declarative Syntax Helpers")

# Valley

Python extensible schema validations and declarative syntax helpers.

[![Unittests](https://github.com/capless/valley/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/capless/valley/actions/workflows/main.yml)

## Installation

```shell
pip install valley
```

## Getting Started

```python
import valley as v


class Animal(v.Schema):
    name = v.StringProperty(required=True)
    species = v.StringProperty(required=True)
    color = v.StringProperty(required=True)
    meal_type = v.StringProperty()
    age = v.IntegerProperty(required=True)
    
frog = Animal(name='Kermit',species='frog',color='green',meal='carnivore',age=1)
frog.validate()
```

