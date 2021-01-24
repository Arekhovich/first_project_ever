import json

from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from manager.forms import CommentForm
from manager.models import LikeComment, Comment, Book
from manager.models import LikeBookUser as RateBookUser
from rest_framework.generics import DestroyAPIView, RetrieveUpdateAPIView, CreateAPIView, ListCreateAPIView
from manager.permissions import IsAuthor
from manager.serializers import CommentSerializer, LikeCommentUserSerializer, BookSerializer


class AddLikeComment(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeCommentUserSerializer
    queryset = LikeComment.objects.all()

    def get_object(self):
        user = self.request.user
        comment_id = self.kwargs['pk']
        query_set = LikeComment.objects.filter(user=user, comment_id=comment_id)
        if query_set.exists():
            return query_set.first()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            LikeComment.objects.create(user=request.user, comment_id=self.kwargs['pk'])
        else:
            obj.delete()
        return Response({"likes": LikeComment.objects.filter(comment_id=self.kwargs['pk']).count()})



def add_rate(request):
    if request.user.is_authenticated:
        stars = int(request.GET.get('rate'))
        RateBookUser.objects.create(user=request.user, book_id=request.GET.get('slug'), rate=stars)
        result_rate = float(Book.objects.get(slug=request.GET.get('slug')).rate)
        return JsonResponse({'rate': result_rate}, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'user is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

def delete_book(request):
    if request.user.is_authenticated:
        book = Book.objects.get(slug=request.GET.get('slug'))
        if request.user in book.authors.all():
            book.delete()
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'user is not author'}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({'error': 'user is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

def add_comment_ajax(request):
    if request.user.is_authenticated:
        text = request.POST.get('new_comment')
        author = request.user
        slug = request.POST.get('slug')
        Comment.objects.create(text=text, author=author, book_id=slug)
        return JsonResponse({'text': text}, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'user is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteComment(DestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentSerializer
    # lookup_field = "id" можно не использовать, т.к. используем pk
    queryset = Comment.objects.all()

class CreateBook(ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    queryset = Book.objects.all()



