from . import (RequiredValidator, StringValidator,
                MaxLengthValidator, MinLengthValidator,
                IntegerValidator, MaxValueValidator,
                MinValueValidator, FloatValidator,
                DateValidator, DateTimeValidator, BooleanValidator,
                SlugValidator,EmailValidator
                         )


class VariableMixin(object):

    def get_validators(self):
        if self.required:
            self.validators.insert(0, RequiredValidator())


class CharVariableMixin(VariableMixin):

    def get_validators(self):
        VariableMixin.get_validators(self)
        self.validators.append(StringValidator())
        if self.kwargs.get('min_length'):
            self.validators.append(MinLengthValidator(
                self.kwargs.get('min_length')))

        if self.kwargs.get('max_length'):
            self.validators.append(MaxLengthValidator(
                self.kwargs.get('max_length')))


class SlugVariableMixin(CharVariableMixin):

    def get_validators(self):
        super(SlugVariableMixin, self).get_validators()
        self.validators.append(SlugValidator())


class EmailVariableMixin(CharVariableMixin):

    def get_validators(self):
        super(EmailVariableMixin, self).get_validators()
        self.validators.append(EmailValidator())


class NumericVariableMixin(VariableMixin):

    def get_validators(self):
        VariableMixin.get_validators(self)
        if self.kwargs.get('max_value'):
            self.validators.append(MaxValueValidator(
                self.kwargs.get('max_value')))

        if self.kwargs.get('min_value'):
            self.validators.append(MinValueValidator(
                self.kwargs.get('min_value')))


class IntegerVariableMixin(NumericVariableMixin):

    def get_validators(self):
        super(IntegerVariableMixin, self).get_validators()
        self.validators.insert(0, IntegerValidator())


class FloatVariableMixin(NumericVariableMixin):

    def get_validators(self):
        super(FloatVariableMixin, self).get_validators()
        self.validators.insert(0, FloatValidator())


class DateMixin(VariableMixin):

    def get_validators(self):
        super(DateMixin, self).get_validators()
        self.validators.insert(0, DateValidator())


class DateTimeMixin(VariableMixin):

    def get_validators(self):
        super(DateTimeMixin, self).get_validators()
        self.validators.insert(0, DateTimeValidator())


class BooleanMixin(VariableMixin):

    def get_validators(self):
        self.validators = [BooleanValidator()]
