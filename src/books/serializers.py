from rest_framework import serializers
from books.models import Books, Copies
from categories.serializer import CategorySerializer
from authors.serializer import AuthorSerializer

class BookReadSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    authors = AuthorSerializer(many=True)
    class Meta:
        model = Books
        fields = "__all__"


class BookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"

    def validate_annee_publication(self, value):
        if value <= 0 :
            raise serializers.ValidationError('Année invalide')
        return value
    
    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError('ISBN non valide !')
        return value
    

class CopieReadSerializer(serializers.ModelSerializer):
    book = BookReadSerializer()
    class Meta:
        model = Copies
        fields = "__all__"

class CopieWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copies
        fields = "__all__"