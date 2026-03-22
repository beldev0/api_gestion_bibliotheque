from django.db import models
from  django.contrib.auth.models import AbstractUser, BaseUserManager

import uuid
# Create your models here.
# class Subscriptions(models.Model):
#     member 
#

def rename_file(self, filename):
    ext = filename.split('.')[-1]
    return f"profil/{uuid.uuid4()}.{ext}"

def rename_etudiant_carte_file(self, filename):
    ext = filename.split('.')[-1]
    return f"carte/{uuid.uuid4()}.{ext}"


class CustomManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have an email address")

        email=self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True  

        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=255, blank=True, null=True)
    carte_etudiant = models.ImageField(blank=True, null=True, upload_to=rename_etudiant_carte_file)
    role = models.CharField(choices=[
        ('manager', 'Manager'),
        ('librarian', 'Librarian'),
        ('member', 'Member')
    ], default='member', max_length=9)
    birthday = models.DateField()
    status = models.CharField(choices=[
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('bloque', 'Bloqué'),
        ('expire', 'Expiré')
        ('attente', 'En attente')
    ], default="actif", max_length=8)
    profil = models.ImageField(upload_to=rename_file, blank=True, default=None, null=True),


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomManager()


class InvitationToken(models.Model):
    jti = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    