from django.urls import path
from .views import *

urlpatterns = [
    path('createLoan/', create_loan),
    path('closeLoan/<int:id>/', closeLoan)
]