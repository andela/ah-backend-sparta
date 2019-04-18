from django.urls import path

from .views import (
    ProfileCreateAPIView, 
    ProfileDetailAPIView, 
    FollowCreateDestroyAPIView,
    FollowersListView,
    FollowingListView
)

app_name = 'profiles'
urlpatterns = [
    path('profiles/<str:username>', ProfileDetailAPIView.as_view()),
    path('profiles/', ProfileCreateAPIView.as_view()),
    path('profiles/<str:username>/follow', FollowCreateDestroyAPIView.as_view()),
    path('profiles/<str:username>/followers', FollowersListView.as_view()),
    path('profiles/<str:username>/following', FollowingListView.as_view()),
]
