from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class Cover(models.IntegerChoices):
        HARD = 1
        SOFT = 2

    title = models.CharField(
        max_length=255,
        help_text="Title of the book",
    )
    author = models.CharField(
        max_length=255,
        help_text="Author of the book",
    )
    cover = models.PositiveSmallIntegerField(
        choices=Cover.choices,
        help_text="Cover of the book",
    )
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=0)],
        help_text="Copies of the book available for borrowing (positive)",
    )
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(limit_value=0)],
        help_text="Amount of daily fee when book is borrowed (positive)",
    )

    def __str__(self):
        return f'"{self.title}" by {self.author}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
