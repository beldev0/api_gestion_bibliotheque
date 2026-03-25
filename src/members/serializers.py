from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import isValidToken
from .models import InvitationToken, Subscriptions
from datetime import date

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=150, write_only=True)
    invite_token = serializers.CharField(required=False, allow_blank=True, write_only=True, max_length=255)
    subscription_plan = serializers.CharField(required=False, allow_blank=True)

    class Meta:     
        model = User
        fields = ['last_name', 'first_name', 'email', 'phone', 'address', 'carte_etudiant', 'birthday', 'status', 'profil', 'password', 'confirm_password','invite_token', 'role', 'subscription_plan']
        extra_kwargs = {
            'role': {'read_only':True},
            'status' : {'read_only':True},
            'password' : {'write_only': True}
        }

    def validate_phone(self, value):
        if not value.startswith('01'):
            raise serializers.ValidationError('Le numéro de télephone doit commencer par 01')
        
        if len(value) != 10:
            raise serializers.ValidationError('Taille du numéro non conforme')
        
        return value
    
    def validate_invite_token(self, value):
        if value:
            jti, err = isValidToken(value)
            if err:
                raise serializers.ValidationError(err)
            return jti

    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Les mots de passe ne sont pas pareil')
        
        if not 'invite_token' in data :
            if  'subscription_plan' not in data or data['subscription_plan'] == "":
                raise serializers.ValidationError({"subscription_plan": "'Vous devez choisir une formule'"})
            
            if data['subscription_plan'] == 'student' and 'carte_etudiant' not in data:
                raise serializers.ValidationError({"carte_etudiant": "Vous devez soumettre votre carte etudiant"})

            if data['subscription_plan'] not in ['student', 'premium', 'standard'] :
                raise serializers.ValidationError({"subscription_plan": "Plan d'abonnement non reconnu"})

        return data
    

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        if 'invite_token' in validated_data:
            jti =  validated_data.pop('invite_token')
            invitation = InvitationToken.objects.get(jti=jti)

            invitation.is_used = True
            invitation.save()
            validated_data['role'] = "librarian"
        
        if 'carte_etudiant' in validated_data:
            validated_data['status'] = 'attente'
        
        if 'subscription_plan' in validated_data:
            subscription_plan = validated_data.pop('subscription_plan')

        
        print(validated_data)

        user = User.objects.create_user(**validated_data)

        if subscription_plan:
            subs = Subscriptions.objects.create(member = user, formule=subscription_plan)
            print(subs.id)
        return user
    

class changePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    old_password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Mot de passe non conforme")
        return data
    
    def validate_old_password(self, value):
        user =  self.context['request'].user
        if user:
            if not user.check_password(value):
                raise serializers.ValidationError('Ancien mot de passe incorrect')
            return value
        raise serializers.ValidationError('Vous devez être authentifié !')
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = Subscriptions
        fields = ['id', 'status', 'date_deb', 'date_end', 'formule', 'remaining']

    def get_remaining(self, instance):
        today = date.today()
        delta = instance.date_end - today
        return delta.days

class UserProfileSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'email', 'phone', 'address', 'birthday', 'status', 'profil', 'role', 'subscription']
        extra_kwargs = {'role': {'read_only':True}, 'status':{'read_only':True}, 'id': {'read_only':True}}

    def validate_phone(self, value):
        if not value.startswith('01'):
            raise serializers.ValidationError('Le numéro de télephone doit commencer par 01')
        
        if len(value) != 10:
            raise serializers.ValidationError('Taille du numéro non conforme')
        
        return value