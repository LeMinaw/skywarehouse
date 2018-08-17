from django.db   import models
from django.core.validators import MaxValueValidator

class GradeField(models.PositiveSmallIntegerField):
    def __init__(self, max_grade=10, *args, **kwargs):
        validator = MaxValueValidator(max_grade)
        super().__init__(validators=[validator], *args, **kwargs)
