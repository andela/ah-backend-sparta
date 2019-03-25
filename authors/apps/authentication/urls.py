from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='update-user'),
    path('users/', RegistrationAPIView.as_view(), name='register-user'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
]
