from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import SubscriptionPlanRules
from .serializers import SubscriptionPlanRulesSerializer
# Create your views here.

class SubscriptionRulesViewSet(ModelViewSet):
    queryset = SubscriptionPlanRules.objects.all()
    serializer_class = SubscriptionPlanRulesSerializer