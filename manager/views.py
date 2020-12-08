from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from manager.models import Book, LikeBookUser, LikeComment, Comment


def hello(request, name="filipp", digit=None):
    if digit is not None:
        return HttpResponse(f"digit is {digit}")
    return HttpResponse(f"hello {name}")


class MyPage(View):
    def get(self, request):
        context = {}
        context["books"] = Book.objects.prefetch_related("authors", "comments").annotate(count=Count("likes1"))
        context["comments"] = Comment.objects.annotate(count=Count("likes_com"))
        return render(request, "index.html", context)


class AddLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            LikeBookUser.objects.create(user=request.user, book_id=id)

        return redirect("the-main-page")

class AddCommentLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            LikeComment.objects.create(user=request.user, comment_id=id)

        return redirect("the-main-page")

# Create your views here.
