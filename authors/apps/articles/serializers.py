from rest_framework import serializers
from . import models
from authors.apps.profiles.serializers import ProfileSerializer
from .models import Article
from authors.apps.comments.models import Comment
from authors.apps.comments.serializers import CommentDetailSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)

    class Meta:
        fields = '__all__'
        model = models.Article
        read_only_fields = ['author', 'slug']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    comments = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'author', 'title', 'description', 'slug', 'body', 'createdAt', 'updatedAt', 'comments']
        model = models.Article
        read_only_fields = ['author', 'slug']

    def get_comments(self, obj):
        comment = Article.objects.get(title=obj)
        comment_query_set = Comment.objects.filter(article_id=comment.id, parent_id=None)
        comments = CommentDetailSerializer(comment_query_set, many=True).data
        return comments
