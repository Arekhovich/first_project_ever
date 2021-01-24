from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from manager.models import Comment, LikeComment, Book


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class LikeCommentUserSerializer(ModelSerializer):
    class Meta:
        model = LikeComment
        fields = "__all__"

class BookSerializer(ModelSerializer):
    date = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['title', 'text', 'date']
    def get_date(self, obj):
        return obj.date