from django.db import models

# Create your models here.
class SubscriptionPlanRules(models.Model):
    price = models.IntegerField()
    formule = models.CharField(max_length=50, unique=True)
    extended_count = models.IntegerField()
    loan_days_duration = models.IntegerField()
    lifetime = models.IntegerField(default=365)
    max_book = models.IntegerField()
