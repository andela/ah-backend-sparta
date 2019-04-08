from django.shortcuts import render
from rest_framework import generics ,status
from .models import Article
from authors.apps.profiles.models import Profile
from . import serializers
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from .serializers import ArticleSerializer 

class ListCreateArticle(generics.ListCreateAPIView):
    """
    An authenticated user can GET all articles
    or can create an article
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer

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
    
    