from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

from Common.models import Entity


class BillType(Entity):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_day = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31)
    ])

    def __str__(self):
        return self.name


class Bill(Entity):
    type = models.ForeignKey(BillType, on_delete=models.PROTECT)
    due_date = models.DateField()
    paid_date = models.DateField(null = True, blank = True)

    def __str__(self):
        return f'{self.name} ({self.due_date})'

    @property
    def owner(self):
        return self.type.owner

    @property
    def name(self):
        return f'{self.type.name}'

    @property
    def due_month(self):
        return self.due_date.month


    def save(self, *args, **kwargs):
        # Restringir cada conta a ser criada a apenas uma vez por mês
        month = self.due_date.month

        same_month_bills = Bill.objects.filter(type = self.type, due_date__month = month)
        result_count = same_month_bills.count()
        if result_count == 0 or result_count == 1 and same_month_bills[0] == self:
            return super().save(*args, **kwargs)

        raise Exception('Only one bill per month is allowed for each type.')
