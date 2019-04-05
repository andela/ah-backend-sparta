from .test_base import BaseTestCase
from authors.apps.authentication.serializers import (
    LoginSerializer, UserSerializer
)
from unittest.mock import patch, MagicMock, PropertyMock

from rest_framework.serializers import ValidationError

class TestLoginSerializer(BaseTestCase):
    """
    class to handles user model tests
    """
    def test_email_not_provided_to_validate_function(self):
        """
        Method to test if email is not provided to validate function in serializers
        """
        data_no_email = {
            "email":None,
            "password":"user@12345"
        }
        with self.assertRaises(ValidationError) as e:
            LoginSerializer().validate(data_no_email)
        self.assertEqual(e.exception.args[0], 'An email address is required to log in.')

    def test_password_not_provided_to_validate_function(self):
        """
        Method to test if password is not provided to validate function in serializers
        """
        data_no_password = {
            "email":"user@gmail.com",
            "password":None
        }
        with self.assertRaises(ValidationError) as e:
            LoginSerializer().validate(data_no_password)
        self.assertEqual(e.exception.args[0], 'A password is required to log in.')

    def test_user_is_not_active(self):
        """
        Method to test if user is  not active 
        """
        user_password_and_email = {
            "email":"user@gmail.com",
            "password":"user@1234"
        }
       
        class MockAuthenticate:
            is_active = False

            @classmethod
            def __call__(cls,  *args, **kwargs):
                return cls

        with patch('authors.apps.authentication.serializers.authenticate', new_callable=MockAuthenticate),\
            self.assertRaises(ValidationError) as e:
        
            LoginSerializer().validate(user_password_and_email)

        self.assertEqual(e.exception.args[0], 'This user has been deactivated.')

    def test_update_user_data(self):
        """
        Method to test update user data
        """
        class UpdateUserInstance:
           
            def save(self):
                pass
            def set_password(self, password): 
                pass
                
        data_to_update_user = {
            "email":"user@gmail.com,",
            "password":"user@123",
            "username":"usher123"
        }

        class_instance = UpdateUserInstance()
        self.assertEqual(UserSerializer().update(class_instance, data_to_update_user), class_instance)

