from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
    GenericAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from rest_framework.permissions import IsAuthenticated
from .renderers import CommentJSONRenderer
from .models import Comment
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    CommentChildSerializer,
    CommentRepliesSerializer
)


class CommentDetailAPIView(RetrieveAPIView):
    renderer_classes = (CommentJSONRenderer,)
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'


class ChildCommentAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentChildSerializer


class CommentListAPIView(ListAPIView):
    """
    class to get all comments
    """
    permission_classes = (
        IsAuthenticated,
    )
    renderer_classes = (CommentJSONRenderer,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentReplyDetailsView(ListAPIView):
    """
    class to retrieve all replies about a given comment
    """
    permission_classes = (
        IsAuthenticated,
    )
    queryset = Comment.objects.all()
    serializer_class = CommentRepliesSerializer
    lookup_field = 'parent_id'

    def get_queryset(self):
        return self.queryset.filter(parent_id=self.kwargs.get('parent_id')).order_by('createdAt')

class CommentEditHistoryView(GenericAPIView):
    """
    history of comment for particular user
    """
    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        comment_history = comment.history.all()

        edit_history = []
        for edit in list(comment_history):
            
            
            comment_edit_history = {
                "date": edit.history_date,
                "id": edit.history_id,
                "comment_body": edit.body
            }
            edit_history.append(comment_edit_history)
            
        comment = Comment.objects.get(pk=pk)
       
        return Response({
            "history": edit_history,
            "number_of_edits": len(edit_history) - 1
        }, status=status.HTTP_200_OK)
