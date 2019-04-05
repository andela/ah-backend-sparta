from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, FacebookAuthApiView, GoogleAuthApiView, TwitterAuthApiView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='update-user'),
    path('users/register/', RegistrationAPIView.as_view(), name='register-user'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/login/facebook', FacebookAuthApiView.as_view(), name='facebook'),
    path('users/login/google', GoogleAuthApiView.as_view(), name='google'),
    path('users/login/twitter', TwitterAuthApiView.as_view(), name='twitter')
]
