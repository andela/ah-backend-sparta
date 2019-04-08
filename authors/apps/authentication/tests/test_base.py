"""
Test base module
"""
from rest_framework.test import APITestCase, APIClient
from authors.apps.authentication.tests.test_data import (
    login_credentials_data, 
    login_data
    )

class BaseTestCase(APITestCase):
    """
    Class to define a testbase class
    """
    token = None

    def setUp(self):
        """
         Method to handle data to be setup before running tests
        """
        self.client = APIClient()
        self.token = f'Bearer {self.generate_jwt_token()}'


    def generate_jwt_token(self):

        if not BaseTestCase.token:
            self.client.post('/api/users/register/', login_credentials_data, format='json')
            response1 = self.client.post('/api/users/login/', login_data, format='json')

            BaseTestCase.token = response1.data["token"]
        return BaseTestCase.token 

    def create_user(self, user_data):
        self.client.post('/api/users/register/', user_data, format='json')
        response1 = self.client.post('/api/users/login/', user_data, format='json')

        return f'Bearer {response1.data["token"]}'