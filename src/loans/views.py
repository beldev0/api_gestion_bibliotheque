from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoanSerializer
from .models import Loans
from datetime import date
# Create your views here.
@api_view(['POST'])
def create_loan(request):
    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def closeLoan(request, id):
    lo = get_object_or_404(Loans, id =id)
    ecart = (lo.date_end - date.today()).days
    if ecart < 0:
        lo.status = 'lateness' 
    else:
        lo.status = 'rendered'
    lo.date_back = date.today()
    lo.book.status = 'disponible'
    lo.book.save()
    lo.save()
    serializer =  LoanSerializer(lo)
    return Response(serializer.data)
    