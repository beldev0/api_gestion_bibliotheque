from rest_framework import serializers
from .models import Authors

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = "__all__"