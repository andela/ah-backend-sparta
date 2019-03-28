"""
Test base module
"""
from rest_framework.test import APITestCase, APIClient


class BaseTestCase(APITestCase):
    """
    Class to define a testbase class
    """

    def setUp(self):
        """
         Method to handle data to be setup before running tests
        """
        self.client = APIClient()
    