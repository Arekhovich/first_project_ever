from django.http import HttpResponse, JsonResponse
from rest_framework import status

from manager.forms import CommentForm
from manager.models import LikeComment, Comment, Book
from manager.models import LikeBookUser as RateBookUser


def add_like2comment(request):
    if request.user.is_authenticated:
        comment_id = request.GET.get('comment_id')
        LikeComment.objects.create(user=request.user, comment_id=comment_id)
        comment = Comment.objects.get(id=comment_id)
        count_likes = comment.likes
        return JsonResponse({'likes': count_likes}, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'user is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


def delete_comment(request):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=request.GET.get('comment_id'))
        if request.user == comment.author:
            comment.delete()
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'user is not author'}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({'error': 'user is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)



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
