from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .utils import get_token_for_user
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q, Count, Sum
from loans.models import Loans
from django.db.models.functions import Coalesce
from django.db.models import Prefetch
from .models import Subscriptions
User = get_user_model()

# Create your views here.
@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        get_token_for_user(refresh, user)
        
        tokens = {
            'refresh': str(refresh),
            'access_token': str(refresh.access_token)
        }
        return Response({
            'user' : serializer.data,
            **tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def changePassword(request):
    serializer = changePasswordSerializer(data=request.data, context={'request':request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Mot de passe modifié avec succès"} ,status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def editUserProfil(request):
    user = request.user

    if request.method ==  "PUT":
        serializer = UserProfileSerializer(user, data=request.data)
    else:
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def me(request):
    user_id = request.user.id

    user = User.objects.prefetch_related('subscription').get(id=user_id)
    serializer = UserProfileSerializer(user)
    token = request.auth
    print(token['formule'])
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def allUsers(request):
    users = User.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def userCanBorrow(request, id):
    active_subs = Subscriptions.objects.filter(status='actif')
    user = User.objects.prefetch_related(Prefetch('subscription', queryset=active_subs)).annotate(
    total_loan=Count(
        'loan',
        filter=Q(loan__status='pending')
    ),
    total_penalty=Coalesce(Sum(
        'loan__penalty__amount',
        filter=Q(loan__penalty__status='nsold')
    ), 0)).get(id=id)

    serializer = UserCanBorrowSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

    