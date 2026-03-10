from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializer import CategorySerializer
from .models import Categories

# Create your views here.

class CategoryViewset(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

    def perform_destroy(self, instance):


        return super().perform_destroy(instance)