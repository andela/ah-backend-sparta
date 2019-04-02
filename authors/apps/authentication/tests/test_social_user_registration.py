from unittest.mock import patch
from .test_base import BaseTestCase
from .test_data import (invalid_facebook_token, invalid_google_token, invalid_twitter_tokens, 
                        one_twitter_token, social_reg_data, social_reg_no_email_data)
from authors.apps.authentication.social_registration import register_social_user, settings
from authors.apps.authentication.tests.test_data import test_user_data


class TestSocialAuth(BaseTestCase):

    def test_invalid_facebook_token(self):
        response = self.client.post('/api/users/login/facebook', invalid_facebook_token, format='json')
        self.assertEqual(response.data['auth_token'], 'Please provide a valid token')

    def test_invalid_google_token(self):
        response = self.client.post('/api/users/login/google', invalid_google_token, format='json')
        self.assertEqual(response.data['auth_token'], 'Please provide a valid token')

    def test_invalid_twitter_tokens(self):
        response = self.client.post('/api/users/login/twitter', invalid_twitter_tokens, format='json')
        self.assertEqual(response.data['auth_token'], 'Please provide valid tokens')

    def test_one_twitter_token(self):
        response = self.client.post('/api/users/login/twitter', one_twitter_token, format='json')
        self.assertEqual(response.data['auth_token'], 'Please provide two tokens')

    def test_with_valid_google_token_succeeds(self):

        class MockGoogleAuth:

            @classmethod
            def verify_oauth2_token(cls, token, request):
                return {
                    'iss': 'accounts.google.com',
                    'email': 'test@email.com',
                    'given_name': 'testname'
                }

        with patch('authors.apps.authentication.serializers.id_token', new_callable=MockGoogleAuth):
            response = self.client.post('/api/users/login/google', invalid_google_token, format='json')
            self.assertEqual(response.data['auth_token']['email'], 'test@email.com')


    def test_with_invalid_iss_fails(self):

        class MockGoogleAuth:

            @classmethod
            def verify_oauth2_token(cls, token, request):
                return {
                    'iss': 'invalid_iss.com',
                    'email': 'test@email.com',
                    'given_name': 'testname'
                }

        with patch('authors.apps.authentication.serializers.id_token', new_callable=MockGoogleAuth):
            response = self.client.post('/api/users/login/google', invalid_google_token, format='json')
            self.assertEqual(response.data['auth_token'], 'Please provide a valid token')

    
    def test_with_valid_facebook_token_succeeds(self):

        class MockFacebookAuth:

            def __init__(self, *args, **kwargs):
                pass
            
            @classmethod
            def request(cls, link):
                return {
                    'email': 'testfb@testmail.com',
                    'name': 'testfbname'
                }
            
            def __call__(self, *args, **kwargs):
                return self

        with patch('authors.apps.authentication.serializers.facebook.GraphAPI', new_callable=MockFacebookAuth):
            response = self.client.post('/api/users/login/facebook', invalid_facebook_token, format='json')
            self.assertEqual(response.data['auth_token']['email'], 'testfb@testmail.com') 


    def test_with_valid_twitter_token_succeeds(self):

        class MockTwitterAuth:

            def __init__(self, *args, **kwargs):
                pass    
        
            class VerifyCredentials:

                def __init__(self, *args, **kwargs):
                    pass
                
                @property
                def __dict__(self):
                    return {
                        'email': 'testtw@testmail.com',
                        'screen_name': 'testtwname'
                    }
            
            def __call__(self, *args, **kwargs):
                return self

        with patch('authors.apps.authentication.serializers.twitter.Api', new_callable=MockTwitterAuth):
            response = self.client.post('/api/users/login/twitter', invalid_twitter_tokens, format='json')
            self.assertEqual(response.data['auth_token']['email'], 'testtw@testmail.com') 


class TestSocialRegistration(BaseTestCase):

    def test_social_registration_with_no_email(self):
        email = social_reg_no_email_data['email']
        username = social_reg_no_email_data['username']
        response = register_social_user(email, username)
        self.assertEqual(response, 'no email provided')

    def test_social_registration_with_no_SOCIAL_USER_PASS(self):

        class MockSettings:
            SOCIAL_USER_PASS = False
        
        with patch('authors.apps.authentication.social_registration.settings', new_callable=MockSettings):
            response = register_social_user('email', 'username')
            self.assertEqual(response, 'password not provided')

    def test_social_registration_with_an_existing_user(self):
        self.create_user(test_user_data)
        response = register_social_user(test_user_data['user']['email'], 'username')
        self.assertEqual(response, 'A user with this email already exists, Please login using that account')


    def test_social_registration(self):
        email = social_reg_data['email']
        username = social_reg_data['username']
        response = register_social_user(email, username)
        response2 = register_social_user(email, username)
        self.assertEqual(response["email"], "test@testmail.com")
        self.assertEqual(response2["username"], "testname")
    