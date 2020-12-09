from django.db.models import Count, Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from manager.models import Book, LikeBookUser, LikeComment, Comment


def hello(request, name="filipp", digit=None):
    if digit is not None:
        return HttpResponse(f"digit is {digit}")
    return HttpResponse(f"hello {name}")


# class MyPage(View):
#     def get(self, request):
#         context = {}
#         books = Book.objects.prefetch_related("authors", "comments")
#         context["books"] = books.annotate(count=Count("users_like"))
#         context["comments"] = Comment.objects.annotate(count=Count("likes_com"))
#         return render(request, "index.html", context)
#
#         #добавление лайков для комментов вместо context["comments"]
#         #comment_query=Comment.objects.annotate(count_like=Count("users_like")).select_related("author")
#         #comments = Prefetch("comments", comment_query)
#         #context["books"] = Book.objects.prefetch_related("authors", comments).annotate(count_like=Count("users_like"))


class MyPage(View):
    def get(self, request):
        context = {}
        comment_query = Comment.objects.annotate(count_like=Count("likes_com")).select_related("author")
        comments = Prefetch("comments", comment_query)
        books = Book.objects.prefetch_related("authors", comments)
        context["books"] = books
        context["rate"] = "3"
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

class BookDetail(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        return render(request, "book_detail.html", {"book": book})
# Create your views here.
