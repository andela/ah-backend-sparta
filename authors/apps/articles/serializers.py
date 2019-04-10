from rest_framework import serializers
from . import models
from authors.apps.profiles.serializers import ProfileSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    class Meta:
        fields = '__all__'
        model = models.Article
        read_only_fields = ['author','slug']

class ArticleLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["user", "article", "likes", "createdAt"]
        model = models.ArticleLikeDislike
        extra_kwargs = {
            'user': {'write_only': True},
            'article': {'write_only': True},
        }
        unique_together=["user", "likes"]