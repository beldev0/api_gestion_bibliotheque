from rest_framework_simplejwt.tokens import Token, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from  datetime import timedelta
from .models import InvitationToken

class InvitationTokenClass(Token):
    lifetime = timedelta(hours=24)
    token_type = "Invitation"

def createInvitationToken(email):
    token = InvitationTokenClass()
    token["email"] = email
    jti = token['jti']

    InvitationToken.objects.create(jti=jti, email=email)

    return str(token)

def isValidToken(token_string):
    try:
        token = InvitationTokenClass(token_string)
        jti = token['jti']

        try:
            invitation = InvitationToken.objects.get(jti=jti)
        except InvitationToken.DoesNotExist:
            return None, "Token non reconnu"
        
        if invitation.is_used:
            return None, "Token d'invitation expiré"
        
        return jti, None
    except TokenError as e:
        return None, str(e)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['role'] = user.role
    refresh.access_token['email'] = user.email
    refresh.access_token['role'] = user.role

    return {
        'refresh' : str(refresh),
        'access_token' : str(refresh.access_token)
    }

