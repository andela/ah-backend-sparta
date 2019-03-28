from .test_base import BaseTestCase
from authors.apps.authentication.models import UserManager
from unittest.mock import patch, MagicMock, PropertyMock
from authors.apps.authentication.models import User

class TestUserModel(BaseTestCase):
    """
    class to handles user model tests
    """
    def test_username_not_provided_on_creating_user(self):
        """
        Method to test if user is created without providing a username
        """
        with self.assertRaises(TypeError):
            UserManager().create_user(username=None, email="user@gmail.com")

    def test_email_not_provided_on_creating_user(self):
        """
        Method to test if user is created without providing an email
        """
        with self.assertRaises(TypeError):
            UserManager().create_user(username="user22", email=None)

    def test_password_not_provided_on_creating_super_user(self):
        """
        Method to test if super user is create without a password
        """
        with self.assertRaises(TypeError):
            UserManager().create_superuser(username="user22", email="user@gmail.com", password=None)

    def test_if_password_is_provided_when_creating_super_user(self):
        """
        Method to test if super user is created with a password
        """
        class MockCreateUser:
            is_superuser = False
            is_staff = False

            @classmethod
            def __call__(cls,  *args, **kwargs):
                return cls()
        
            def save(self):
                pass

        with patch('authors.apps.authentication.models.UserManager.create_user', new_callable=MockCreateUser):
            user = UserManager().create_superuser(username="user22", email="user@gmail.com", password="user@123")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.save(), None)




    
