from django.shortcuts import render
from rest_framework import generics ,status
from .models import Article, ArticleLikeDislike
from authors.apps.profiles.models import Profile
from . import serializers
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from .serializers import ArticleSerializer 
from .pagination import ArticlePageNumberPagination

class ListCreateArticle(generics.ListCreateAPIView):
    """
    An authenticated user can GET all articles
    or can create an article
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    pagination_class = ArticlePageNumberPagination

    def create(self,request):
        article=request.data
    
        serializer=self.serializer_class(data=article)
        
        author = Profile.objects.get(username=self.request.user.username)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=author, slug=Article.get_slug(article.get('title')))
        return Response({"article":serializer.data})

class RetrieveUpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    """
    Only the authenticated and owner of the article has 
    access to edit/delete the article. An authenticated
    user can get article by Id.
    """
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    
class ArticleLikeDislikeView(generics.GenericAPIView):
    """
    Article should be liked or disliked and toggle
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleLikeDislikeSerializer

    def post(self, request, pk):
        article = Article.objects.filter(pk=pk).first()
        likes = request.data["likes"]
        # querty = ArticleLikeDislike.objects.filter(article_id=article.id, 
        #                                                 user_id=request.user.id) 
        # liked_article = querty if querty else 
        query = ArticleLikeDislike.objects.filter(article_id=article.id, 
                                                        user_id=request.user.id) 
        liked_article = query if query is not None else liked_article.update(likes=False)
        # if liked_article:
            #if row does not exist, create row with data below
            #if likes == True:
        serializer_data = self.serializer_class(data={
            "user": request.user.id,
            "article": article.id,
            "likes": likes
        })

        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()
        #data is going to be returned in the response

        data = {
            "article": article.title,
            "username": request.user.username,
            "details": serializer_data.data
        }
        # else:
        #    #like is toggled by user when endpoint is triggered twice OR ++
        #     value = not (liked_article.first().likes)
        #     liked_article.update(likes=value)
        #     data = {
        #         "article": article.title,
        #         "username": request.user.username,
        #         "details": {
        #             "likes": liked_article.first().likes,
        #             "created_at": liked_article.first().created_at
        #         }
        #     }
        # updates the number of likes and dislikes of a given article
        likes = ArticleLikeDislike.objects.filter(article_id=article.id, likes=True)
        dislikes = ArticleLikeDislike.objects.filter(article_id=article.id, likes=False)
        Article.objects.filter(pk=pk).update(likes=likes.count() , dislikes=dislikes.count())

        return Response(data, status=status.HTTP_200_OK)