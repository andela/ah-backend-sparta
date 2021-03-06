from django.contrib.auth import authenticate
from django.conf import settings
import re

from rest_framework import serializers

import facebook
import twitter
from google.oauth2 import id_token
from google.auth.transport import requests

from .models import User
from .social_registration import register_social_user
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    email = serializers.EmailField()
    username = serializers.CharField()

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    # making token read-only
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def validate_password(self, password):
        """
        Method to validate user posted password
        """
        if len(password.split()) > 1:
            raise serializers.ValidationError(
                "Password should not contain spaces"
            )
        elif not re.search(r"[0-9]", password) or not re.search(r"[A-Z]", password) or not re.search(
            r"[@_!#$%^&*()<>?/\|}{~:]", password):
            raise serializers.ValidationError(
                "Invalid Password format,It should have an Uppercase letter,digit and special character"
            )
       

    def validate_email(self, email):
        """
        Method to validate the email input by a new user signing up
        It ensures that the email being used for signing up was not already used by another user.
        """

        check_email = User.objects.filter(email=email)
        if check_email.exists():
            raise serializers.ValidationError("Provided email address already exists, please provide a different one")
        

    def validate_username(self, username):
        """
        Method to validate that the username is not owned by another user
        """
        regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
        check_username = User.objects.filter(username=username)
        if check_username.exists():
            raise serializers.ValidationError("Provided username already exist, please provide a different one")
        elif regex.search(username):
            raise serializers.ValidationError("should not contain special characters @_!#$%^&*()<>?/\|}{~:")
        elif  len(username.split()) > 1:
            raise serializers.ValidationError(
                "Username should not contain spaces"
            )

    def validate(self, attrs):

        values = self.initial_data
        keys = self.fields.keys()

        for key in values.copy():
            values.pop(key) if key not in keys else None

        return values

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        # 'is_verified' tells us if the user account has been verified by clicking 
        # the link sent to their email 
        verified_user = User.objects.filter(email=email).first()
        if not verified_user.is_verified:
            raise serializers.ValidationError(
                'This user has not been verified.'
            )
        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128 
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and 
        # `max_length` properties too, but that isn't the case for the token
        # field.


    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance

class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(allow_blank=False)

    def validate_email(self, data):
        email = data.get('email', None)
        if email is None:
            raise serializers.ValidationError(
                'Email is required'
                )
        return data

class ConfirmPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    class Meta:
        model = User
        fields = ('password','confirm_password')

    
class SocialAuthSerializer(serializers.Serializer):
    """
    Social Authentication parent class
    """
    auth_token = serializers.CharField()
    
    def validate_auth_token(self, auth_token):
        user_data = self.get_user_data(auth_token)
        return user_data


class FacebookAuthSerializer(SocialAuthSerializer):
    """
    Inherits from SocialAuthSerializer
    """
    def get_user_data(self, auth_token):
        """
        This function decodes the received token into data required from the user, 
        all this with the help of facebook's GraphAPI. Data received includes email,
        name and profile picture
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            user_profile = graph.request('/me?fields=name,email,picture')
            
            email = user_profile['email']
            name = user_profile['name']

            username = name.replace(' ', '_')

            return register_social_user(email, username)

        except:
            return 'Please provide a valid token'
                

class GoogleAuthSerializer(SocialAuthSerializer):
    """
    Inherits from SocialAuthSerializer
    """
    def get_user_data(self, auth_token):
        """
        To parse and verify an ID Token issued by Google’s OAuth 2.0 authorization
        verify_oauth2_token function is used
        check ['iss'] key to make sure that the token is from google
        """
        try:
            user_profile = id_token.verify_oauth2_token(auth_token, requests.Request())
            
            if user_profile['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            email = user_profile['email']
            username = user_profile['given_name']

            return register_social_user(email, username) 
           
        except ValueError:
            return 'Please provide a valid token'


class TwitterAuthSerializer(SocialAuthSerializer):
    """
    Inherits from SocialAuthSerializer
    """
    def get_user_data(self, auth_token):
        """
        Twitter works with 4 tokens, two of which are received by this function
        This function creates an instance of twitter.api
        and then api.VerifyCredentials() returns a user object
        """

        if len(auth_token.split(" ")) != 2:
            return "Please provide two tokens"

        access_token_key = auth_token.split(" ")[0]
        access_token_secret = auth_token.split(" ")[1]

        try:
            api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY,
                                consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                                access_token_key = access_token_key,
                                access_token_secret = access_token_secret)
            user_profile = api.VerifyCredentials(include_email=True).__dict__

            email = user_profile["email"]
            username = user_profile["screen_name"]

            return register_social_user(email, username)

        except twitter.error.TwitterError:
            return 'Please provide valid tokens'
