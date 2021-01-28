from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from manager.models import Comment, LikeComment, Book, User


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UserSerialize(ModelSerializer):
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = User
        fields = ["username", "comment_set"]


class LikeCommentUserSerializer(ModelSerializer):
    class Meta:
        model = LikeComment
        fields = "__all__"

class BookSerializer(ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    authors = UserSerialize(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['title', 'text', 'date', 'authors']

    def get_date(self, obj):
        return obj.date

    def save(self, **kwargs):
        book = super().save
        book.authors.add(kwargs['data'])
        book.save()

