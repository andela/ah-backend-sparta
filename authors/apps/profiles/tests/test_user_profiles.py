from authors.apps.authentication.tests.test_base import BaseTestCase
from rest_framework import status
from .test_data import(
    register_user1_data,
    register_user2_data,
    update_user_profile_data1,
    update_user_profile_data2,
    update_user_profile_data_with_wrong_url,
    update_user_profile_data3,
    register_user3_data 

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

    def test_user_following_another_user(self):
        """
        Method to test user can follow another user
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response4 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response3.data["message"], "You are now following maria22")
        self.assertEqual(response4.data["message"], "You are now following joan22")
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)

    def test_user_can_unfollow_another_user(self):
        """
        Method to test a user can unfollow another user
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response4 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        response5 = self.client.delete('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        
        self.assertEqual(response5.data["message"], "You have unfollowed  maria22")
        self.assertEqual(response5.status_code, status.HTTP_204_NO_CONTENT)


    def test_user_cant_unfollow_themselves(self):
        """
        Method to test a user unfollowing themselves
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response4 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        response5 = self.client.delete('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        
        self.assertEqual(response5.data["errors"][0], "You can not unfollow your self")
        self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_unfollow_a_user_for_two_times(self):
        """
        Method to test a user unfollowing a user they have already unfollowed
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response4 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        response5 = self.client.delete('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response6 = self.client.delete('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        
        self.assertEqual(response6.data["errors"][0], "You have already unfollowed  maria22")
        self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_view_users_your_following(self):
        """
        Method to getting a list of users one is following
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response4 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        response5 = self.client.get('/api/profiles/maria22/followers', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response5.data[0]["username"], "joan22")
        self.assertEqual(response5.status_code, status.HTTP_200_OK)

    def test_view_users_that_are_following_you(self):
        """
        Method to test getting alist of users that are following you
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response4 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        response5 = self.client.get('/api/profiles/maria22/following', HTTP_AUTHORIZATION=user_token1,  format='json')
        
        self.assertEqual(response5.data[0]["username"], "joan22")
        self.assertEqual(response5.status_code, status.HTTP_200_OK)

    def test_user_to_follow_does_not_exist(self):
        """
        Method to test following a user who does not exist
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22hghghgh/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
       
        self.assertEqual(response3.data["detail"], "Not found.")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    def test_following_a_user_you_already_follow(self):
        """
        Method to test following a user you already follow
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token2,  format='json')
        response4 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        response5 = self.client.post('/api/profiles/joan22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response5.data["errors"][0], "You already follow this user")

    def test_a_user_following_themselves(self):
        """
        Method to test following a user you already follow
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.post('/api/profiles/maria22/follow', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response3.data["errors"][0], "You can not follow your self")

    def test_user_is_not_following_anyone(self):
        """
        Method to test user does not follow any one
        """
        user_token1 = self.create_user(register_user3_data)
        response1 = self.client.put('/api/profiles/claire22', update_user_profile_data3, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.get('/api/profiles/claire22/following', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response2.data["errors"][0], "You are currently not following anyone")
    

    def test_user_does_not_have_followers(self):
        """
        Method to test user does not user following them
        """
        user_token1 = self.create_user(register_user3_data)
        response1 = self.client.put('/api/profiles/claire22', update_user_profile_data3, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.get('/api/profiles/claire22/followers', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response2.data["errors"][0], "You dont have any followers")

    def test_a_given_user_does_not_have_followers(self):
        """
        Method to test user does not have followers
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.get('/api/profiles/joan22/followers', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response3.data["errors"][0], "joan22 does not have any followers")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_given_user_does_not_have_users_following(self):
        """
        Method to test user does not have users they are following
        """
        user_token1 = self.create_user(register_user1_data)
        user_token2 = self.create_user(register_user2_data)
        response1 = self.client.put('/api/profiles/joan22', update_user_profile_data1, HTTP_AUTHORIZATION=user_token1,  format='json')
        response2 = self.client.put('/api/profiles/maria22',  update_user_profile_data2, HTTP_AUTHORIZATION=user_token2, format='json')
        response3 = self.client.get('/api/profiles/joan22/following', HTTP_AUTHORIZATION=user_token1,  format='json')
        self.assertEqual(response3.data["errors"][0], "joan22 is currently not following anyone")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)