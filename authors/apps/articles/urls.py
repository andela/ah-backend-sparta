from django.urls import path
from .views import (
    ListCreateArticle, 
    RetrieveUpdateDestroyArticle,
    RetrieveArticleCommentDetails,
    CommentCreateAPIView,
    CreateReplyToCommentAPIView,
    DeleteUpdateCommentAPIView,
    ArticleLikeDislikeView,
    FavoriteArticle,
    RatingsView
)

app_name = "article_application"
urlpatterns = [
    path('articles/', ListCreateArticle.as_view(), name='list-articles'),
    path('articles/<slug>', RetrieveUpdateDestroyArticle.as_view(), name='auth-articles'),
    path('articles/<slug>/comments/', CommentCreateAPIView.as_view(), name='create-article-comment'),
    path('articles/<slug>/comments/<int:pk>/reply', CreateReplyToCommentAPIView.as_view(),
         name='create-article-comment-reply'),
    path('articles/<slug>/comments/<int:pk>', DeleteUpdateCommentAPIView.as_view(), name='delete-update-comment'),
    path('articles/<slug>/comments', RetrieveArticleCommentDetails.as_view(), name='articles-comments-details'),
    path('articles/<slug>/like', ArticleLikeDislikeView.as_view(), name='like-dislike'),
    path('articles/<slug>/favorite', FavoriteArticle.as_view(), name='favorite'),
    path("articles/<slug>/rate", RatingsView.as_view(), name="rating"),
]
