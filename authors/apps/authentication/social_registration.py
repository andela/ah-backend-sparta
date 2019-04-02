from django.conf import settings
from .models import User
from django.contrib.auth import authenticate


def register_social_user(email, username):
    """
    Registers user if they don't exist or log them 
    in if they don't
    """

    if not email:
        return 'no email provided'

    password = settings.SOCIAL_USER_PASS
    if not password:
        return 'password not provided' 

    check_user = User.objects.filter(email=email, registration_platform='app')
    if check_user:
        return 'A user with this email already exists, Please login using that account'

    check_social_user = User.objects.filter(email=email, registration_platform='social')
    if check_social_user:
        user = authenticate(username=email, password=password)
        user.is_active
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
    
    new_user = {            
        'email': email,
        'username': username,
        'password': password           
    }
    User.objects.create_user(**new_user)
    user = authenticate(username=email, password=password)
    user.registration_platform = 'social'
    user.is_active
    user.save()
    return {
        'email': user.email,
        'username': user.username,
        'token': user.token
    }
