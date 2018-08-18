from django.utils.deconstruct import deconstructible
from django.core.exceptions   import ValidationError

@deconstructible
class MaxFileSizeValidator(object):
    message = 'Max allowed file size is %(max_size)s.'
    code = 'file_too_big'

    def __init__(self, max_size=10*1024**2, message=None, code=None):
            self.max_size = max_size
            if message is not None:
                self.message = message
            if code is not None:
                self.code = code

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(self.message, code=self.code, params={'max_size': self.max_size})

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.max_size == other.max_size and
            self.message == other.message and
            self.code == other.code
        )
