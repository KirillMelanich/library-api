from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class Cover(models.IntegerChoices):
        HARD = 1
        SOFT = 2

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.PositiveSmallIntegerField(choices=Cover.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=0)],
    )

    def __str__(self):
        return f'"{self.title}" by {self.author}'


