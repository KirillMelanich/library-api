from django.db import models

from book.models import Book
from user.models import Customer


class Borrowing(models.Model):
    borrow_date = models.DateField(
        help_text="Borrow date",
    )
    expected_return_date = models.DateField(
        help_text="Expected return date "
        "(value should be greater or equal then borrow_date)"
    )
    actual_return_date = models.DateField(
        blank=True,
        null=True,
        help_text="Actual retutn date "
        "(value should be greater or equal then borrow_date)",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
        help_text="ID of borrowed book",
    )
    user = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="borrowings",
        help_text="ID of customer",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    expected_return_date__gte=models.F("borrow_date")
                ),
                name="check_expected_return_date",
                violation_error_message="Expected return date should be"
                " greater or equal then borrow date",
            ),
            models.CheckConstraint(
                check=models.Q(actual_return_date__isnull=True)
                | models.Q(actual_return_date__gte=models.F("borrow_date")),
                name="check_actual_return_date",
                violation_error_message="Actual return date should be "
                "greater or equal then borrow date",
            ),
        ]

    def __str__(self):
        return f"Borrowing {self.id}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
