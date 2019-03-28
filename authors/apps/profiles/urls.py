from django.urls import path

from .views import ProfileCreateAPIView

app_name = 'profiles'
urlpatterns = [
    # path('profiles/<str:username>', ProfileRetrieveAPIView.as_view()),
    path('profiles/', ProfileCreateAPIView.as_view()),

]