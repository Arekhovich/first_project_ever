from math import ceil

from django.contrib.auth import login, logout
from django.db.models import Count, Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.db.models import Avg

from manager.forms import BookForm, CustomAuthenticationForm
from manager.models import Book, LikeComment, Comment
from manager.models import LikeBookUser as RateBookUser
from django.contrib.auth.forms import AuthenticationForm


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
        context['books'] = Book.objects.prefetch_related("authors", comments)
        context['range'] = range(1, 6)
        context['form'] = BookForm()
        return render(request, "index.html", context)

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {'form': CustomAuthenticationForm()})

    def post(self, request):
        user = CustomAuthenticationForm(data=request.POST)
        if user.is_valid():
            login(request, user.get_user())
        return redirect("the-main-page")


def logout_user(request):
    logout(request)
    return redirect("the-main-page")

class AddCommentLike(View):
    def get(self, request, slug, location=None):
        if request.user.is_authenticated:
            com_id = Comment.objects.get(book__slug=slug).id
            LikeComment.objects.create(user=request.user, comment_id=com_id)
        if location is None:
            return redirect("the-main-page")
        else:
            return redirect('book-detail', slug=slug)

class AddRate2Book(View):
    def get(self, request, slug, rate, location=None):
        if request.user.is_authenticated:
            book_id = Book.objects.get(slug=slug).id
            RateBookUser.objects.create(user=request.user, book_id=book_id, rate=rate)
        if location is None:
            return redirect("the-main-page")
        return redirect('book-detail', slug=slug)


class BookDetail(View):
    def get(self, request, slug):
        comment_query = Comment.objects.annotate(count_like=Count("likes_com")).select_related("author")
        comments = Prefetch("comments", comment_query)
        book = Book.objects.prefetch_related("authors", comments).get(slug=slug)
        return render(request, "book_detail.html", {"book": book, "rate": [1, 2, 3, 4, 5]})

class AddBook(View):
    def post(self, request):
        if request.user.is_authenticated:
            bf = BookForm(data=request.POST)
            book = bf.save(commit=True)
            book.authors.add(request.user)
            book.save()
        return redirect("the-main-page")
# Create your views here.
