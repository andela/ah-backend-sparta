
from django.urls import path

from .views import (
    CommentListAPIView,
    CommentDetailAPIView,
    CommentReplyDetailsView
)

app_name = 'comments'


urlpatterns = [
    path('comments', CommentListAPIView.as_view(), name='list'),
    path('comments/<int:parent_id>/replies', CommentReplyDetailsView.as_view(), name='comment-replies'),
    path('comments/<int:pk>', CommentDetailAPIView.as_view(), name='comment-detail'),
]