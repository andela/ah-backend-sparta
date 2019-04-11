from rest_framework import generics, status
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authors.apps.comments.models import Comment
from authors.apps.comments.serializers import CommentSerializer
from authors.apps.profiles.models import Profile
from . import serializers
from .models import Article
from .pagination import ArticlePageNumberPagination
from .permissions import IsOwnerOrReadOnly


class ListCreateArticle(generics.ListCreateAPIView):
    """
    An authenticated user can GET all articles
    or can create an article
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    pagination_class = ArticlePageNumberPagination

    def create(self, request):
        article = request.data

        serializer = self.serializer_class(data=article)

        author = Profile.objects.get(username=self.request.user.username)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=author, slug=Article.get_slug(article.get('title')))
        return Response({"article": serializer.data})


class RetrieveUpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    """
    Only the authenticated and owner of the article has 
    access to edit/delete the article. An authenticated
    user can get article by Id.
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    lookup_field = 'slug'


class RetrieveArticleCommentDetails(generics.RetrieveAPIView):
    """
    View Class to get specific article commennts
    """
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleDetailSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    """
    Class to handle creation of comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(slug=self.kwargs.get('slug'))

        comment =  request.data.get("comment")
        author = request.user.id

        serialized_data = self.serializer_class(data=comment)

        serialized_data.is_valid(raise_exception=True)
        serialized_data.save(article_id=article.id, author_id=author)

        return Response(
            data=serialized_data.data, status=status.HTTP_201_CREATED

        )


class CreateReplyToCommentAPIView(generics.CreateAPIView):
    """
    Class to handle creation of comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(slug=self.kwargs.get('slug'))
        comment = request.data.get("comment")
        author = request.user.id

        serialised_data = self.serializer_class(data=comment)
        serialised_data.is_valid(raise_exception=True)
        serialised_data.save(article_id=article.id, author_id=author, parent_id=self.kwargs.get('pk'))
        return Response(
            data=serialised_data.data, status=status.HTTP_200_OK

        )


class DeleteUpdateCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    class to delete a comment on an article
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def delete(self, request, *args, **kwargs):
        """
        Method to delete a comment
        """
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        if comment.author_id != request.user.id:
            return Response(
                data={'message': 'You can only delete your comment'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment = self.queryset.get(pk=kwargs["pk"])
        comment.delete()
        return Response(
            data={
                "message": "Comment has been successfully deleted"
            }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Method to update a comment
        """

        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))

        data = request.data["comment"]
        if comment.author_id != request.user.id:
            return Response(
                data={'message': 'You can only update your comment'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(
            comment,
            data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
