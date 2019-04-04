"""
Test base module
"""
from django.test import TestCase
from authors.apps.authentication.models import User
from rest_framework.test import APITestCase, APIClient, APILiveServerTestCase
from authors.apps.authentication.tests.test_data import (
    login_credentials_data, 
    login_data
    )

class BaseTestCase(TestCase):
    """
    Class to define a testbase class
    """
    token = None

    def setUp(self):
        """
         Method to handle data to be setup before running tests
        """
        self.client = APIClient()

        self.client.post('/api/users/register/', login_credentials_data, format='json')
        response1 = self.client.post('/api/users/login/', login_data, format='json')
        print('res', response1.data)

        BaseTestCase.token = response1.data["token"]

        self.token = 'Bearer {}'.format(BaseTestCase.token)


    # def generate_jwt_token(self):
    #
    #     if not BaseTestCase.token:
    #         User.objects.create_user(**login_credentials_data)
    #         self.client.post('/api/users/register/', login_credentials_data, format='json')
    #         response1 = self.client.post('/api/users/login/', login_data, format='json')
    #         print('res', response1.data)
    #
    #         BaseTestCase.token = response1.data["token"]
    #     print('token', BaseTestCase.token)
    #     return BaseTestCase.token

    def create_user(self, user_data):
        self.client.post('/api/users/register/', user_data, format='json')
        response1 = self.client.post('/api/users/login/', user_data, format='json')

        return f'Bearer {response1.data["token"]}'
            