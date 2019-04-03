from authors.apps.authentication.tests.test_base import BaseTestCase
from rest_framework import status
from .test_data import(
    register_user1_data,
    register_user2_data,
    update_user_profile_data1,
    update_user_profile_data2,
    update_user_profile_data_with_wrong_url
)

class TestUserProfiles(BaseTestCase):
    """
    Class to handle tests of profile management
    """

    def test_updating_users_profiles(self):
        """
        Method to test updating a user profile
        """
        user_token1 = self.create_user(register_user1_data)
        response1 = self.client.put('/api/profiles/maria22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        
        self.assertEqual(response1.data["username"], "maria22")
        self.assertEqual(response1.data["firstname"], update_user_profile_data1["firstname"])
        self.assertEqual(response1.data["lastname"], update_user_profile_data1["lastname"])
        self.assertEqual(response1.data["bio"], update_user_profile_data1["bio"])
        self.assertEqual(response1.data["image"], update_user_profile_data1["image"])
        self.assertEqual(response1.status_code, status.HTTP_200_OK)



    def test_getting_all_user_profiles(self):
        """
        Method to test getting all user profiles
        """
        user_token1 = self.create_user(register_user1_data)
        
        self.client.put('/api/profiles/maria22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
    
        #Get all user Profiles
        response = self.client.get('/api/profiles/', HTTP_AUTHORIZATION=user_token1, format='json')
        self.assertEqual(response.data["profiles"][0]["username"], "maria22")
        self.assertEqual(response.data["profiles"][0]["firstname"], update_user_profile_data1['firstname'])
        self.assertEqual(response.data["profiles"][0]["lastname"], update_user_profile_data1['lastname'])
        self.assertEqual(response.data["profiles"][0]["bio"], update_user_profile_data1['bio'])
        self.assertEqual(response.data["profiles"][0]["image"], update_user_profile_data1['image'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_getting_specific_user_profile(self):
        """
        Method to test getting a single user profile
        """
        user_token1 = self.create_user(register_user1_data)
        self.client.put('/api/profiles/maria22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')

        #Get all user Profiles
        response = self.client.get('/api/profiles/maria22', HTTP_AUTHORIZATION=user_token1, format='json')
        self.assertEqual(response.data["username"], "maria22")
        self.assertEqual(response.data["firstname"], update_user_profile_data1["firstname"])
        self.assertEqual(response.data["lastname"], update_user_profile_data1["lastname"])
        self.assertEqual(response.data["bio"], update_user_profile_data1["bio"])
        self.assertEqual(response.data["image"], update_user_profile_data1["image"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_updating_profile_which_is_not_theirs(self):
        """
        Method to test whether users are updating a profile that is not their profile
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        self.assertEqual(response1.data["message"], "You can only edit your Profile")
        self.assertEqual(response2.data["message"], "You can only edit your Profile")
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_raise_exception_when_url_is_wrong(self):
        """
        Method to test raise exception incase the image url is invalid
        """
        user_token = self.create_user(register_user2_data)
        response = self.client.put('/api/profiles/joan22', update_user_profile_data_with_wrong_url, HTTP_AUTHORIZATION=user_token,  format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["image"][0].title(), 'Enter A Valid Url.')



    













