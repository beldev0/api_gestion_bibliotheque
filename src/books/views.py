from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
# Create your views here.
from .serializers import *
from .models import *

class BookViewset(ModelViewSet):
    queryset = Books.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] : 
            return BookReadSerializer
        return BookWriteSerializer
    
    # def perform_destroy(self, instance):

    #     return super().perform_destroy(instance)


class CopiesViewset(ModelViewSet):
    queryset = Copies.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CopieReadSerializer
        return CopieWriteSerializer