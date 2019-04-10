from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)

from .models import Comment
from authors.apps.profiles.serializers import ProfileSerializer


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    author = ProfileSerializer(required=False)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields =('id', 'parent', 'reply_count', 'createdAt', 'author')

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'createdAt',
            'author',
        )


class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    author = ProfileSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'reply_count',
            'replies',
            'createdAt',
            'author'
        )

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentRepliesSerializer(ModelSerializer):
    """
    serializer class to get specific replies to a given comment
    """
    author = ProfileSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'createdAt',
            'author',
        )
