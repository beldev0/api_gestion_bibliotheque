from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import CustomUserSerializer
from utils import get_token_for_user
# Create your views here.
@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens =  get_token_for_user(user)
        
        return Response({
            'user' : serializer.data,
            **tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)