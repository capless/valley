from valley.contrib import Schema
from valley.properties import *


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


class NameSchema(Schema):
    _create_error_dict = True
    name = CharProperty(required=True)

    def __unicode__(self):
        return self.name


class Breed(NameSchema):
    pass


class Dog(NameSchema):
    breed = ForeignProperty(Breed,required=True)


class Troop(NameSchema):
    dogs = ForeignListProperty(Dog)
    primary_breed = ForeignProperty(Breed)


cocker = Breed(name='Cocker Spaniel')

cockapoo = Breed(name='Cockapoo')

bruno = Dog(name='Bruno',breed=cocker)

blitz = Dog(name='Blitz',breed=cockapoo)

durham = Troop(name='Durham',dogs=[bruno,blitz],primary_breed=cocker)