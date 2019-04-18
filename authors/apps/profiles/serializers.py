from rest_framework import serializers

from .models import Profile
    


class ProfileSerializer(serializers.ModelSerializer):
    followers_no = serializers.SerializerMethodField()
    following_no = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = ('username','firstname', 'lastname', 'bio', 'image', 'followers_no', 'following_no')
        read_only_fields = ('followers_no', 'following_no')



    def get_followers_no(self, instance):
        '''Method calculates the number of users a user follows'''
        number_of_users_a_user_follows = instance

        return Profile.follows.through.objects.filter(to_profile_id=number_of_users_a_user_follows.pk).count()

    def get_following_no(self, instance):
        '''Method calculates the number of users following a user'''
        number_of_users_following_a_user = instance

        return Profile.followed_by.through.objects.filter(from_profile_id=number_of_users_following_a_user.pk).count()