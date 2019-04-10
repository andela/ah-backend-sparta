"""
Module to test functionality to register a user
"""
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from .test_data import (
    no_login_credentialds_data,
    login_credentials_data,
    empty_string_username,
    empty_string_email,
    empty_string_password,
    invalid_email_data,
    login_data,
    test_user_data,
    invalid_login_data,
    login_data_miss_email,
    login_data_miss_password,
    empty_login_data_object,
    auth_change_password,
    test_user_data_password_change,
    password_contain_spaces,
    username_contain_spaces,
    username_contains_special_characters
)
from .test_base import BaseTestCase


class TestUserRegistration(BaseTestCase):
    """
    class to handle user registration and user login tests
    """

    def test_register_a_user_with_no_data(self):
        """
        Method to test if posted user registration user object contains  no data
        """

        response = self.client.post('/api/users/register/', no_login_credentialds_data, format='json')
        self.assertIn(response.data["errors"]["email"][0], 'This field is required.')
        self.assertIn(response.data["errors"]["username"][0], 'This field is required.')
        self.assertIn(response.data["errors"]["password"][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_contains_spaces(self):
        """
        Method to test if password contains spaces
        """
        response = self.client.post('/api/users/register/', password_contain_spaces, format='json')
        self.assertIn(response.data["errors"]["password"][0], 'Password should not contain spaces')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_username_contains_spaces(self):
        
        """
        Method to test if username contains spaces
        """
        response = self.client.post('/api/users/register/', username_contain_spaces, format='json')
        self.assertIn(response.data["errors"]["username"][0], 'Username should not contain spaces')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_username_contains_special_charcters(self):
        """
        Method to test if username contains spaces
        """
        response = self.client.post('/api/users/register/', username_contains_special_characters, format='json')
        self.assertIn(response.data["errors"]["username"][0], 'should not contain special characters @_!#$%^&*()<>?/\\|}{~:')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_register_a_user_with_data(self):
        """
        Method to test if posted registration user object contains data
        """
        response = self.client.post('/api/users/register/', login_credentials_data, format='json')
        self.assertEqual(response.data["email"], 'testuser@gmail.com')
        self.assertEqual(response.data["username"], 'user')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response1 = self.client.post('/api/users/register/', login_credentials_data, format='json')
        self.assertEqual(response1.data["errors"]["email"][0], 'Provided email address already exists, please provide a different one')
        self.assertEqual(response1.data["errors"]["username"][0], 'Provided username already exist, please provide a different one')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registered_with_empty_string_username(self):
        """
        Method to test if username is an empty string
        """
        response = self.client.post('/api/users/register/', empty_string_username, format='json')
        self.assertIn(response.data["errors"]["username"][0], '"This field may not be blank."')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registered_with_empty_email_string(self):
        """
        Method to test if username is an empty string
        """
        response = self.client.post('/api/users/register/', empty_string_email, format='json')
        self.assertIn(response.data["errors"]["email"][0], '"This field may not be blank."')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registered_with_empty_password_string(self):
        """
        Method to test if username is an empty string
        """
        response = self.client.post('/api/users/register/', empty_string_password, format='json')
        self.assertIn(response.data["errors"]["password"][0], 'This field may not be blank.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registered_with_an_invalid_email(self):
        """
        Method to test if email is an invalid email
        """
        response = self.client.post('/api/users/register/', invalid_email_data , format='json')
        self.assertIn(response.data["errors"]["email"][0], 'Enter a valid email address.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_successfully_with_valid_data(self):
        """
        Method to test if user successfully logs in using valid credentials
        """
        response = self.client.post('/api/users/register/', login_credentials_data, format='json')
        self.client.get('/api/users/verify/'+"?token="+ response.data['token'])

        response = self.client.post('/api/users/login/', login_data, format='json')
        self.assertEqual(response.data["email"], 'testuser@gmail.com')
        self.assertEqual(response.data["username"], 'user')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logged_in__with_invalid_data(self):
        """
        Method to test if user  logs in using invalid credentials
        """
        self.client.post('/api/users/', login_credentials_data, format='json')
        response = self.client.post(
            '/api/users/login/', 
            invalid_login_data, format='json'
        )
        self.assertIn(response.data["errors"]["error"][0], 'A user with this email and password was not found.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_log_in_credentials_miss_email(self):
        """
        Method to test if email is not added in the login required credentials
        """
        self.client.post('/api/users/', login_credentials_data, format='json')
        response = self.client.post('/api/users/login/', login_data_miss_email, format='json')
        self.assertIn(response.data["errors"]["email"][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_log_in_credentials_miss_password(self):
        """
        Method to test if password is not added in the login required credentials
        """
        self.client.post('/api/users/', login_credentials_data, format='json')
        response = self.client.post('/api/users/login/', login_data_miss_password, format='json')
        self.assertIn(response.data["errors"]["password"][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_log_in_credentials_miss_password_and_email(self):
        """
        Method to test if password is not added in the login required credentials
        """
        self.client.post('/api/users/', login_credentials_data, format='json')
        response = self.client.post('/api/users/login/', empty_login_data_object, format='json')
        self.assertIn(response.data["errors"]["password"][0], 'This field is required.')
        self.assertIn(response.data["errors"]["email"][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_current_user_jwt(self):
        """
        Get current user from JWT
        """
        user_token = self.create_user(test_user_data)
        response2 = self.client.get('/api/user/', HTTP_AUTHORIZATION=user_token, format='json')
        self.assertEqual(response2.data["email"], test_user_data.get('user').get('email'))
        self.assertEqual(response2.data["username"], test_user_data.get('user').get('username'))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_change_password_user_jwt_authenticated(self):
        """
        change password of authenticated user
        """
        # Token = self.token
        # self.client.credentials(HTTP_AUTHORIZATION = self.token)
        # #print(self.token)
        user_token = self.create_user(test_user_data)
        response2 = self.client.put(
            '/api/user/', 
            test_user_data_password_change,
            HTTP_AUTHORIZATION=user_token,format='json'
        )
        self.assertEqual(response2.data["email"], test_user_data.get('user').get('email'))
        self.assertEqual(response2.data["username"], test_user_data.get('user').get('username'))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
    def test_change_password_user_jwt_authenticated_invalid_token(self):
        """
        change password of authenticated user
        """

        invalid_token = 'Bearer hgfgsdyuertgsdtyshjgsdjusdhghjsdyj'

       
        self.client.credentials(HTTP_AUTHORIZATION = invalid_token)

        response2 = self.client.put('/api/user/', auth_change_password,format='json')
        self.assertEqual(response2.data["detail"], 'Invalid authentication. Could not decode token.')

        response2 = self.client.put('/api/user/', auth_change_password,format='json')
        self.assertEqual(response2.data["detail"], 'Invalid authentication. Could not decode token.')

    def test_verify_user(self):
        """ tests if user can be verified on registration with token"""
        res = self.client.post('/api/users/register/', test_user_data, format='json')
        response = self.client.get(
            '/api/users/verify/'+"?token="+res.data['token']
        )
        self.assertEqual(
            response.data['Message'], 
            'Account successfully verified, your free to  now login'
        )
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK
        )

    def test_cannot_verify_user_with_invalid_token(self):
        """ tests if user cannot be verified with invalid token token"""

        class MockUserToken:

            @classmethod
            def decode(cls, token, secret_key):
                return {
                    'id': 1,
                    'exp': 1333
                }

        with patch('authors.apps.authentication.views.jwt', new_callable=MockUserToken):
            response = self.client.get('/api/users/verify/', format='json')
            self.assertEqual(response.data['Message'], 'Something went wrong')

    def test_email_sent_on_registration(self):
            """ """

            class MockUserToken:

                @classmethod
                def decode(cls, token, secret_key):
                    return {
                        'id': 1,
                        'exp': 1333
                    }

            with patch('authors.apps.authentication.views.jwt', new_callable=MockUserToken):
                response = self.client.get('/api/users/verify/', format='json')
                self.assertEqual(response.data['Message'], 'Something went wrong')        
 

