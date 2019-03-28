from django.urls import path

from .views import ProfileCreateAPIView, ProfileDetailAPIView

app_name = 'profiles'
urlpatterns = [
    path('profiles/<str:username>', ProfileDetailAPIView.as_view()),
    path('profiles/', ProfileCreateAPIView.as_view()),
]
