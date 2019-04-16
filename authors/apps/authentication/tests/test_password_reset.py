"""
Module to test password reset
"""
from unittest.mock import patch
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from .test_base import BaseTestCase
from .test_data import test_user_data, reset_data, login_data, password_reset_data, unmatched_password, wrong_reset_email


class TestPasswordReset(BaseTestCase):
    """
    class to handle user password reset
    """
    def test_reset_email_link_sent(self):

        self.client.post(reverse('register-user'),
            data=test_user_data,
            format='json')
        response = self.client.post(reverse('reset-password'), 
            data=reset_data,
            format='json')
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertEquals(response.data['message'],'Password reset link has been sent to your Email')

    def test_reset_email_does_not_exist(self):

        self.client.post(reverse('register-user'),
            data=test_user_data,
            format='json')
        response = self.client.post(reverse('reset-password'), 
            data=wrong_reset_email,
            format='json')
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'],"Email does not exist")

    def test_password_reset(self):

        res = self.client.post(reverse('register-user'),
            data=test_user_data,
            format='json')
        token = res.data["token"]
        response = self.client.put(reverse('password-change', kwargs={'token':token}), 
            data=password_reset_data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Password has been reset")      
    
    def test_password_not_matching(self):
      
        res =  self.client.post(reverse('register-user'),
            data=test_user_data,
            format='json')
        token = res.data["token"]
        response = self.client.put(reverse('password-change', kwargs={'token':token}), 
            data=unmatched_password,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Passwords do not match") 
    

