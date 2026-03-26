from rest_framework import serializers
from .models import SubscriptionPlanRules

class SubscriptionPlanRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlanRules
        fields = '__all__'

    def validate_price(self, value):
        if value < 0 :
            raise serializers.ValidationError('Vous devez entrer un prix correct')  
        return value
    
    def validate_extended_count(self, value):
        if value < 0 :
            raise serializers.ValidationError('Vous devez entrer un nombre correct')  
        return value
    
    def validate_loan_days_duration(self, value):
        if value < 0 :
            raise serializers.ValidationError('Vous devez entrer une durée correct')  
        return value

    def validate_lifetime(self, value):
        if value < 0 :
            raise serializers.ValidationError('Vous devez entrer une durée correct')  
        return value
    
    def validate_formule(self, value):
        if not value:
            raise serializers.ValidationError('Vous devez nommer la formule')
        return value.lower() 