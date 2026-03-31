from django.db import models
from django.conf import settings
from books.models import Copies
# Create your models here.
class Loans(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='loan')
    book = models.ForeignKey(Copies, on_delete=models.PROTECT)
    date_deb = models.DateField(auto_now_add=True)
    date_end = models.DateField()
    date_back = models.DateField(blank=True, null=True)
    extended_count = models.IntegerField()
    status = models.CharField(choices=[
        ('lost', 'LOST'),
        ('rendered', 'RENDERED'),
        ('lateness', 'LATENESS'),
        ('pending', 'PENDING')
    ], default='pending')


class Penalty(models.Model):
    emprunt = models.OneToOneField(Loans, on_delete=models.PROTECT, related_name='penalty')
    status = models.CharField(choices=[
        ('sold', 'SOLD'),
        ('nsold', 'NOT SOLD')
    ], default='nsold')
    amount = models.IntegerField()


class PaymentHistory(models.Model):
    amount = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    penalty = models.ForeignKey(Penalty, on_delete=models.PROTECT, related_name='payment')