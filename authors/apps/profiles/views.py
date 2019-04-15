from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from rest_framework import serializers
from rest_framework.response import Response

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileCreateAPIView(ListAPIView):
    """
    class to create a profile
    """
    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request, format=None):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=dict(profiles=serializer.data), status=status.HTTP_200_OK)


class ProfileDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), user__username=self.kwargs.get('username')
        )

    def put(self, request, *args, **kwargs):
        profile = self.get_object()

        if profile.user_id != request.user.id:
            return Response(
                data={'message': 'You can only edit your Profile'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(profile, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ProfileSerializer(profile).data)


class FollowCreateDestroyAPIView(CreateAPIView, DestroyAPIView):
    """
    Class to handle user following another
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Method to follow an author
        """
        follower_user = request.user.profile
        followed_user = get_object_or_404(Profile, username=self.kwargs.get('username'))
        if follower_user.pk is followed_user.pk:
            raise serializers.ValidationError(
                'You can not follow your self'
            )
        if followed_user.user_is_already_followed_by_you(follower_user):
            raise serializers.ValidationError('You already follow this user')
        follower_user.follow(followed_user)
        serializer = self.serializer_class(followed_user, context={
            'request': request
        })
        return Response(data={"message": "You are now following "+ followed_user.username}, 
        status=status.HTTP_201_CREATED)

    def delete(self, request, username=None):
        """
        Method to unfollow an author one was following
        """
        follower_user = request.user.profile
        followed_user = get_object_or_404(Profile, username=self.kwargs.get('username'))
        if follower_user.pk is followed_user.pk:
            raise serializers.ValidationError(
                'You can not unfollow your self'
            )
        if followed_user.user_is_already_followed_by_you(follower_user):
            follower_user.unfollow(followed_user)
            follower_user.save()
            followed_user.save()
            serializer = self.serializer_class(followed_user, context={
                'request': request
            })
            return Response(data={"message":"You have unfollowed  "+ followed_user.username}, 
            status=status.HTTP_204_NO_CONTENT)
        raise serializers.ValidationError('You have already unfollowed  ' + followed_user.username )
       


class FollowersListView(ListAPIView):
    """
    class to handle the getting of users following you
    """
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self, *args, **kwargs):
        user_profile = get_object_or_404(Profile, username=self.kwargs.get('username'))
        username = self.kwargs.get('username')
        profiles = Profile.objects.filter(follows=user_profile.id).count()
        if profiles < 1:
            if self.request.user.username == username:
                raise serializers.ValidationError(
                    "You dont have any followers"
                )
            if self.request.user.username != username:
                raise serializers.ValidationError(
                    username + " does not have any followers"
                )
        return Profile.objects.filter(follows=user_profile.id)

class FollowingListView(ListAPIView):

    """
    class to handle getting of users you follow
    """
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self, *args, **kwargs):
        user_profile = get_object_or_404(Profile, username=self.kwargs.get('username'))
        username = self.kwargs.get('username')
        profiles = Profile.objects.filter(followed_by=user_profile.id).count()
        
        if profiles < 1:
            if self.request.user.username == username:
                raise serializers.ValidationError(
                    "You are currently not following anyone"
                )
            if self.request.user.username != username:
                raise serializers.ValidationError(
                    username + " is currently not following anyone"
                )
        return Profile.objects.filter(followed_by=user_profile.id)