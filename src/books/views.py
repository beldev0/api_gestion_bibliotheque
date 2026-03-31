from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
from .serializers import *
from .models import *

class BookViewset(ModelViewSet):
    queryset = Books.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] : 
            return BookReadSerializer
        return BookWriteSerializer
    
    def perform_destroy(self, instance):
        if instance.copies.exists():
            print(instance.copies)
            raise ValidationError('Ce livre possède des exemplaires')
        return super().perform_destroy(instance)


class CopiesViewset(ModelViewSet):
    queryset = Copies.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CopieReadSerializer
        return CopieWriteSerializer
    
    # def perform_destroy(self, instance):

    #     return super().perform_destroy(instance)



@api_view(['GET'])
def get_book(request, code):
    try:
        book = Copies.objects.get(code=code)
    except Copies.DoesNotExist:
        return Response({'error': 'Livre non existant'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CopieReadSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)