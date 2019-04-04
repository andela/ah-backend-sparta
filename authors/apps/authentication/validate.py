"""
Module to validate posted user registration data
"""
import re
from rest_framework import serializers
from rest_framework.response import Response
from authors.apps.authentication.models import User


def validate_registration(user_data):
    """
    Method to handle validation of user registration data
    :param user_data:
    :return:
    """
    if check_if_the_required_keys_are_provided(user_data):
        raise serializers.ValidationError(
            dict(inputs_fields=[
                {
                    'username':
                        'Please provide a username , because it is required field'
                },
                {
                    'email': 'Please provide an email address, because it is required field'
                },
                {
                    'password': 'Please provide a password, because its a required field'
                }
            ])

        )
    elif check_if_username_and_email_not_provided(user_data):
        raise serializers.ValidationError(
            dict(inputs_fields=[
                {
                    'username':
                        'Please provide a username , because it is required field'
                },
                {
                      'email': 'Please provide an email address, because it is required field'
                }
            ])

        )
    elif check_if_username_and_password_not_provided(user_data):
        raise serializers.ValidationError(
            dict(inputs_fields=[
                {
                    'username':
                        'Please provide a username , because it is required field'
                },
                {
                    'password': 'Please provide a password, because its a required field'
                }
            ])

        )
    elif check_if_email_and_password_not_provided(user_data):
        raise serializers.ValidationError(
            dict(inputs_fields=[
                {
                    'email': 'Please provide an email address, because it is required field'
                },
                {
                    'password': 'Please provide a password, because its a required field'
                }
            ])
        )

    elif check_for_username_key_in_posted_data(user_data):
        raise serializers.ValidationError(
            {
                'username':
                    'Please provide a username , because it is required field'
            }
        )
    elif check_for_email_key_in_posted_data(user_data):
        raise serializers.ValidationError(
            {
                'email': 'Please provide an email address, because it is required field'
            }
        )
    elif check_for_password_key_in_posted_data(user_data):
        raise serializers.ValidationError(
            {
                'password': 'Please provide a password, because its a required field'
            }
        )

    elif check_if_user_user_provided_a_invalid_email(user_data):
        raise serializers.ValidationError(
            {
                'email': 'Please provide a valid email address'
            }
        )
    elif check_user_registration_email_already_exists(user_data):
        raise serializers.ValidationError(
            {
                'email': 'Provided email address already exists, please provide a different one'
            }
        )
    elif check_user_registration_username_already_exists(user_data):
        raise serializers.ValidationError(
            {
                'username': 'Provided username already exist, please provide a different one'
            }
        )
    elif check_if_password_length_is_less_than_eight(user_data):
        raise serializers.ValidationError(
            {
                'password': 'Password should not be less than 8 characters long'
            }
        )
    elif check_if_password_is_alphanumeric(user_data):
        raise serializers.ValidationError(
            {
                'password': 'Invalid Password format,It should have an Uppercase letter,digit and special character'
            }
        )

    elif not check_if_posted_username_contains_space_in_the_middle(user_data):
        raise serializers.ValidationError(
            {
                'username': 'Username should not contain spaces'

            }
        )
    elif not check_if_posted_data_password_contains_space_in_the_middle(user_data):
        raise serializers.ValidationError(
            {
                'password': 'Password should not contain spaces'

            }
        )

    elif not check_if_posted_username_and_password_contains_spaces_in_the_middle(user_data):
        raise serializers.ValidationError(
            dict(inputs_fields=[
                {
                    'username':
                        'Username should not contain spaces'
                },
                {
                    'password': 'Password should not contain spaces'
                }
            ])
        )
    elif check_if_username_contains_special_characters(user_data):
        raise serializers.ValidationError(
            {
                'username': 'should not contain special characters @_!#$%^&*()<>?/\|}{~:'

            }
        )


def check_for_username_key_in_posted_data(user_registration_data):
    """
    Method to check whether the username exist in the posted user object
    :param user_registration_data:
    :return: decriptive validation error messages
    """
    username = user_registration_data.get("username", None)

    if not username:
        return True


def check_for_email_key_in_posted_data(user_registration_data):
    """
    Method to check whether the email exist in the posted user object
    :param user_registration_data:
    :return: decriptive validation error messages
    """
    email = user_registration_data.get("email", None)

    if not email:
        return True


def check_for_password_key_in_posted_data(user_registration_data):
    """
    Method to check whether the username exist in the posted user object
    :param user_registration_data:
    :return: decriptive validation error messages
    """
    password = user_registration_data.get("password", None)

    if not password:
        return True


def check_if_the_required_keys_are_provided(user_registration_data):
    """
    Method to check whether the username, email and password do not exist in the posted user object
    :param user_registration_data:
    :return: decriptive validation error messages
    """
    username = user_registration_data.get("username", None)
    email = user_registration_data.get("email", None)
    password = user_registration_data.get("password", None)

    if not password and not username and not email:
        return True


def check_if_username_and_email_not_provided(user_registration_data):
    """
    Method to check whether both username and email are not provided
    :param user_registration_data:
    :return:
    """
    username = user_registration_data.get("username", None)
    email = user_registration_data.get("email", None)

    if not username and not email:
        return True


def check_if_username_and_password_not_provided(user_registration_data):
    """
    Method to check whether both username and email are not provided
    :param user_registration_data:
    :return:
    """
    username = user_registration_data.get("username", None)
    password = user_registration_data.get("password", None)

    if not username and not password:
        return True


def check_if_email_and_password_not_provided(user_registration_data):
    """
    Method to check whether both email and password are not provided
    :param user_registration_data:
    :return:
    """
    email = user_registration_data.get("email", None)
    password = user_registration_data.get("password", None)

    if not email and not password:
        return True


def check_if_user_user_provided_a_invalid_email(user_registration_data):
    """
    Method to check whether user provided email is invalid
    :param user_registration_data:
    :return: True
    """
    email = user_registration_data.get("email", None)
    pattern = re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
    if not pattern.match(email):
        return True


def check_user_registration_email_already_exists(user_registration_data):
    """
    Method to check whether user provided email already exists
    :param user_registration_data:
    :return: True
    """
    email = user_registration_data.get("email", None)
    user = User.objects.filter(email=email).count()

    if user >= 1:
        return True


def check_user_registration_username_already_exists(user_registration_data):
    """
    Method to check whether user provided username already exists
    :param user_registration_data:
    :return: True
    """
    username = user_registration_data.get("username", None)
    user1 = User.objects.filter(username=username).count()

    if user1 >= 1:
        return True


def check_if_password_length_is_less_than_eight(user_registration_data):
    """
    Method to check if password length is less than eight
    :param user_registration_data:
    :return: True
    """
    password = user_registration_data.get("password", None)
    if len(password) < 8:
        return True


def check_if_password_is_alphanumeric(user_registration_data):
    """
    Method to check if user password is alphanumeric
    :param user_registration_data:
    :return:
    """
    password = user_registration_data.get("password", None)
    if not re.search(r"[0-9]", password) or not re.search(r"[A-Z]", password) or not re.search(
            r"[@_!#$%^&*()<>?/\|}{~:]", password):
        return True


def check_if_posted_username_contains_space_in_the_middle(user_registration_data):
    """
    Method to check if posted strings contains spaces
    :param user_registration_data:
    :return: True
    """
    username = user_registration_data.get("username", None)
    if not len(username.split()) > 1:
        return True


def check_if_posted_data_password_contains_space_in_the_middle(user_registration_data):
    """
    Method to check if posted strings contains spaces
    :param user_registration_data:
    :return: True
    """
    password = user_registration_data.get("password", None)
    if not len(password.split()) > 1:
        return True


def check_if_posted_username_and_password_contains_spaces_in_the_middle(user_registration_data):
    """
    Method to check if posted strings contains spaces
    :param user_registration_data:
    :return: True
    """
    username = user_registration_data.get("username", None)
    password = user_registration_data.get("password", None)
    if not len(username.split()) > 1 and not len(password.split()) > 1:
        return True


def check_if_username_contains_special_characters(user_registration_data):
    """
    Method to check if username contains special characters
    :param user_registration_data:
    :return: True
    """
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(user_registration_data.get("username", None)):
        return True
    else:
        return False
