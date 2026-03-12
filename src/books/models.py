from django.db import models
from categories.models import Categories
from authors.models import Authors
import uuid

def rename_file(self, filename):
    ext = filename.split('.')[-1]
    return f"books/{uuid.uuid4()}.{ext}"    

# Create your models here.
class Books(models.Model):
    categories = models.ManyToManyField(Categories, related_name='livres')
    authors = models.ManyToManyField(Authors, related_name='livresauthor')
    isbn = models.CharField(max_length=13)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    annee_publication = models.IntegerField()
    langue = models.CharField(max_length=30)
    statut = models.CharField(max_length=12, choices=[('actif', 'ACTIF'), ('archived', 'ARCHIVE')])
    cover = models.ImageField(upload_to=rename_file)


    def __str__(self):
        return f"{self.titre} en  {self.annee_publication}"