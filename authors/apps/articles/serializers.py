from rest_framework import serializers
from . import models
from authors.apps.profiles.serializers import ProfileSerializer
from .models import Article
from authors.apps.comments.models import Comment
from authors.apps.comments.serializers import CommentDetailSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    article_read_time = serializers.CharField(max_length=100, read_only=True)
    favorite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = models.Article
        read_only_fields = ['author', 'slug', 'article_read_time']

    def fetch_usernames(self, users):
        """
        Generate usernames from user profiles
        """
        user_list = []
        for user in users:
            user_list.append(user.username)
        return user_list


    def get_favorite(self, obj):
        """
        returns username rather than user id
        """
        article_fav_users = obj.favorite.all()
        return self.fetch_usernames(article_fav_users)

    def get_average_rating(self, obj):
        return obj.average_rating()


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


class ArticleLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["user", "article", "likes", "createdAt"]
        model = models.ArticleLikeDislike
        extra_kwargs = {
            'user': {'write_only': True},
            'article': {'write_only': True},
        }

class ArticleRatignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleRating
        fields = ["id", "user", "article", "ratings", "created_at"]
        read_only_fields = ["id", "created_at"]

        def validate_ratings(self, value):
            if value < 0 or value > 5:
                raise serializers.ValidationError("Error: Ratings should be between 0 and 5")
            raise value