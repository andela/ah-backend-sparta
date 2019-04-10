from django.urls import path
from .views import ListCreateArticle, RetrieveUpdateDestroyArticle, ArticleLikeDislikeView

app_name = "article_application"
urlpatterns = [
    path('articles/', ListCreateArticle.as_view(), name='list-articles'),
    path('articles/<int:pk>', RetrieveUpdateDestroyArticle.as_view(), name='auth-articles'),
    path('articles/<int:pk>/like', ArticleLikeDislikeView.as_view(), name='like-dislike'),
]
