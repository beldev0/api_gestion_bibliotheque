from django.db import models
import uuid

def rename_file(instance, filename):
    ext = filename.split('.')[1]
    return f"authors/{uuid.uuid4()}.{ext}"  
    
# Create your models here.
class Authors(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    nationality = models.CharField(max_length=30)
    bio = models.TextField()
    image = models.ImageField(upload_to=rename_file)