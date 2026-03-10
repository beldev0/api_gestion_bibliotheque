from django.db import models
from categories.models import Categories

# Create your models here.
class Livres(models.Model):
    categories = models.ManyToManyField(Categories, related_name='livres')