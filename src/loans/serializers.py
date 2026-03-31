from rest_framework import serializers
from .models import Loans
from books.models import Copies
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Sum
from loans.models import Loans
from django.db.models.functions import Coalesce
from rules.models import SubscriptionPlanRules
from books.models import Copies
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loans
        fields = ['id', 'book', 'member', 'date_deb', 'date_end', 'date_back', 'status', 'extended_count', 'member']
        read_only_fields = ['date_deb', 'date_end', 'date_back', 'status', 'extended_count']

    
    def validate(self, data):
        user = User.objects.prefetch_related('subscription').annotate(
            total_loan=Count(
                'loan', 
                filter=Q(loan__status='pending')
            ),
            total_penalty=Coalesce(Sum(
                'loan__penalty__amount',
                filter=Q(loan__penalty__status='nsold')
            ), 0)).get(id=data['member'].id)
        
        print(user.total_loan)
        if user.status != 'actif':
            raise serializers.ValidationError({"error": "Utilisateur non actif"})
        
        if user.total_penalty != 0 :
            raise serializers.ValidationError({"error": "Cet utilisateur a des pénalités"})
        
        active_sub = user.subscription.all().first()
        print(active_sub)

        if not active_sub :
            raise serializers.ValidationError({"error": "Ce utilisateur n'a pas d'abonnement actif"})
        
        
        max_loan = SubscriptionPlanRules.objects.get(formule=active_sub.formule).max_book

        if not user.total_loan < max_loan :
            raise serializers.ValidationError({"error": "Limite d'emprunt atteint"})
        
        book = data['book']
        if book.status != 'disponible':
            raise serializers.ValidationError({"error": "Ce livre n'est pas disponible"})

        data['member'] = user
        return data
    
    def create(self, validated_data):
        user = validated_data.pop('member')

        active_sub = user.subscription.all().first()
        subRules = SubscriptionPlanRules.objects.get(formule=active_sub.formule)
        date_end = (timezone.now() + timedelta(days=subRules.loan_days_duration)).date()
        extended_count = subRules.extended_count

        loan = Loans.objects.create(**validated_data,member = user, date_end=date_end, extended_count=extended_count)

        book = validated_data.get('book')
        book.status = 'emprunte'
        book.save()

        return loan
           
