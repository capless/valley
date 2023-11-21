import valley


class Student(valley.Schema):
    _create_error_dict = True
    name = valley.StringProperty(required=True, min_length=5, max_length=20)
    slug = valley.SlugProperty(required=True, min_length=5, max_length=25)
    email = valley.EmailProperty(required=True)
    age = valley.IntegerProperty(min_value=5, max_value=18)
    gpa = valley.FloatProperty(min_value=0, max_value=4.5)
    date = valley.DateProperty(required=False)
    datetime = valley.DateTimeProperty(required=False)
    active = valley.BooleanProperty()


class StudentB(Student):
    _create_error_dict = False


class NameSchema(valley.Schema):
    _create_error_dict = True
    name = valley.StringProperty(required=True)

    def __unicode__(self):
        return self.name


class Breed(NameSchema):
    pass


class Food(NameSchema):
    pass


class Dog(NameSchema):
    breed = valley.ForeignProperty(Breed, required=True)


class Troop(NameSchema):
    dogs = valley.ForeignListProperty(Dog)
    primary_breed = valley.ForeignProperty(Breed)


cocker = Breed(name='Cocker Spaniel')

cockapoo = Breed(name='Cockapoo')

bruno = Dog(name='Bruno', breed=cocker)

blitz = Dog(name='Blitz', breed=cockapoo)

durham = Troop(name='Durham', dogs=[bruno, blitz], primary_breed=cocker)
