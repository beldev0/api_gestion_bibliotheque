from rest_framework.viewsets import ModelViewSet
from .models import Authors
from .serializer import AuthorSerializer
from rest_framework.exceptions import ValidationError
from books.models import Books

# Create your views here.
class AuthorViewset(ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer

    def perform_destroy(self, instance):
        if instance.livresauthor.exist() :
            raise ValidationError("Ce auteur est associé à des livres")
        return super().perform_destroy(instance)