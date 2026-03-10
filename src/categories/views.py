from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from .serializer import CategorySerializer
from .models import Categories
from livres.models import Livres

# Create your views here.

class CategoryViewset(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

    def perform_destroy(self, instance):
        if instance.livres.exist() :
            raise ValidationError("Suppression impossible. Livre associé existant")
        return super().perform_destroy(instance)