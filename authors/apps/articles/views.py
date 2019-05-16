from django.shortcuts import get_object_or_404, render
from rest_framework import generics ,status
from .models import Article, ArticleLikeDislike, ReadingStats
from authors.apps.profiles.models import Profile
from . import serializers
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authors.apps.comments.models import Comment
from authors.apps.comments.serializers import CommentSerializer
from authors.apps.profiles.models import Profile
from . import serializers
from .models import Article, ArticleRating
from .pagination import ArticlePageNumberPagination
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q


class ListCreateArticle(generics.ListCreateAPIView):
    """
    An authenticated user can GET all articles
    or can create an article
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Article.objects.all().order_by('-createdAt')
    serializer_class = serializers.ArticleSerializer
    pagination_class = ArticlePageNumberPagination
    search_fields = ('author__username', 'title', 'description', 'body', 'tags')

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request
        }

    def create(self, request):
        article = request.data

        serializer = self.serializer_class(data=article, context=self.get_serializer_context())

        author = Profile.objects.get(username=self.request.user.username)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=author, slug=Article.get_slug(article.get('title')))
        return Response({"article": serializer.data})

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        title = self.request.query_params.get('title', None)
        tag = self.request.query_params.get('tag', None)
        keyword = self.request.query_params.get('keyword', None)

        if author:
            queryset = queryset.filter(author__username__icontains=author)
        elif title:
            queryset = queryset.filter(title__icontains=title)
        elif tag:
            queryset = queryset.filter(tags__icontains=tag)
        elif keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(body__icontains=keyword)
            )
            
        return queryset
    



class RetrieveUpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    """
    Only the authenticated and owner of the article has 
    access to edit/delete the article. An authenticated
    user can get article by Id.
    """
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    lookup_field = 'slug'


    def get(self, request, *args, **kwargs):
        user = request.user
        article = self.get_object()
        if not user.is_anonymous:
            ReadingStats.objects.create(article=article, user=user)
        serializer = serializers.ArticleSerializer(article, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    


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
    
class ArticleLikeDislikeView(generics.GenericAPIView):
    """
    Article should be liked or disliked and toggle
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleLikeDislikeSerializer

    def post(self, request, slug):
        article = Article.objects.filter(slug=slug).first()
        likes = request.data["likes"]
        liked_article = ArticleLikeDislike.objects.filter(article_id=article.id, user_id=request.user.id, likes=likes).first()
        
        if liked_article is not None:
            msg = 'You have already liked this article' if likes else 'You have already disliked this article'
            return Response(dict(msg=msg), status=status.HTTP_200_OK)

        liked_article = ArticleLikeDislike.objects.filter(article_id=article.id, user_id=request.user.id).first()
      
        serializer_data = self.serializer_class(data={
            "user": request.user.id,
            "article": article.id,
            "likes": likes
        })

        serializer_data.is_valid(raise_exception=True)

        if not liked_article:
            serializer_data.save()
        else:
            liked_article.likes = likes
            liked_article.save()

        data = {
            "article": article.title,
            "username": request.user.username,
            "details": serializer_data.data
        }
       
        likes = ArticleLikeDislike.objects.filter(article_id=article.id, likes=True)
        dislikes = ArticleLikeDislike.objects.filter(article_id=article.id, likes=False)
        Article.objects.filter(slug=slug).update(likes=likes.count() , dislikes=dislikes.count())

        return Response(data, status=status.HTTP_200_OK)
        
class FavoriteArticle(generics.CreateAPIView):
    """
    User should favorite and unfavorite an article
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer

    def post(self, request, *args, **kwargs):
        favorite_state = request.data.get('favorite')
        if favorite_state is None:
            return Response({'msg': 'Please provide a valid request body'}, status.HTTP_400_BAD_REQUEST)
            
        self.lookup_field = 'slug'
        article = get_object_or_404(self.queryset, slug=self.kwargs.get('slug'))
        returned_status = status.HTTP_200_OK
        if article.favorite.filter(email=request.user.email):
            if favorite_state:
                return Response({'msg': 'You have already favorited this article'}, status.HTTP_400_BAD_REQUEST)
            article.favorite.remove(request.user)
            returned_status = status.HTTP_204_NO_CONTENT
        else:
            if not favorite_state:
                return Response({'msg': 'You have already unfavorited this article'}, status.HTTP_400_BAD_REQUEST)
            article.favorite.add(request.user)
            returned_status = status.HTTP_201_CREATED

        article.save()
        serializer = self.serializer_class(article, context={'request':self.request})
        return Response(serializer.data, status=returned_status)

class RatingsView(generics.CreateAPIView):
    """
    view for rating for articles
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleRatingSerializer

    def post(self, request, **kwargs):
        ratings = ArticleRating.objects.filter(user=request.user.profile, article__slug=kwargs.get('slug'))
        if ratings.count() == 0:
            article = Article.objects.filter(slug=kwargs.get('slug')).first()
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user.profile, article=article)
            return Response(
                {'message': 'Rating received'},
                status = status.HTTP_201_CREATED)
        return Response({"message": "You have already rated."})
        