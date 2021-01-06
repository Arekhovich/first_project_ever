
from django.contrib.auth import login, logout, get_user_model
#from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Prefetch, Exists, OuterRef, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from manager.forms import BookForm, CustomAuthenticationForm, CommentForm, CustomUserCreationForm
from manager.models import Book, LikeComment, Comment, Genre
from manager.models import LikeBookUser as RateBookUser
User = get_user_model()


class MyPage(View):
    def get(self, request):
        context = {}
        books = Book.objects.prefetch_related("authors", "genre")
        gen = Genre.objects.all()

        # Проверка на владельца книги для удаления/редактирования
        if request.user.is_authenticated:
            is_owner = Exists(User.objects.filter(books=OuterRef("pk"), id=request.user.id))
            books = books.annotate(is_owner=is_owner)
        # Добавление постраничного вывода
        page = request.GET.get('page')
        books = Paginator(books, 7)
        try:
            books = books.get_page(page)
        except PageNotAnInteger:
            books = books.page(1)
        except EmptyPage:
            books = books.page(books.num_pages)

        context['books'] = books
        context['range'] = range(1, 6)
        context['form'] = BookForm()
        context['gen'] = gen
        context['page'] = page
        return render(request, "index.html", context)

class PageGenre(View):
    def get(self, request, genre):
        books = Book.objects.filter(genre__name_genre=genre)
        context = {}
        books = books.prefetch_related('authors', 'genre')
        gen = Genre.objects.all()
        if request.user.is_authenticated:
            is_owner = Exists(User.objects.filter(books=OuterRef('pk'), id=request.user.id))
            books = books.annotate(is_owner=is_owner)
        context['books'] = books.order_by('date')
        context['range'] = range(1, 6)
        context['form'] = BookForm()
        context['gen'] = gen
        return render(request, 'page_books_genre.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {'form': CustomAuthenticationForm()})

    def post(self, request):
        user = CustomAuthenticationForm(data=request.POST)
        if user.is_valid():
            login(request, user.get_user())
            return redirect("the-main-page")
        messages.error(request, user.error_messages)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        messages.error(request, form.error_messages)
        return redirect('login')


def logout_user(request):
    logout(request)
    return redirect("the-main-page")


class AddCommentLike(View):
    def get(self, request, id, location=None):
        if request.user.is_authenticated:
            LikeComment.objects.create(user=request.user, comment_id=id)
        if location is None:
            return redirect("the-main-page")
        else:
            slug = Comment.objects.get(id=id).book_id
            return redirect('book-detail', slug=slug)


class AddRate2Book(View):
    def get(self, request, slug, rate, location=None):
        if request.user.is_authenticated:
            RateBookUser.objects.create(user=request.user, book_id=slug, rate=rate)
        if location is None:
            return redirect("the-main-page")
        return redirect('book-detail', slug=slug)


class BookDetail(View):
    def get(self, request, slug):
        comment_query = Comment.objects.select_related("author")
        if request.user.is_authenticated:
            is_owner = Exists(User.objects.filter(comment =OuterRef("id"), id = request.user.id))
            is_liked = Exists(User.objects.filter(liked_comments =OuterRef("pk"), id = request.user.id))
            comment_query = comment_query.annotate(is_owner = is_owner, is_liked=is_liked)
        comments = Prefetch("comments", comment_query)
        book = Book.objects.prefetch_related("authors", comments).get(slug=slug)
        return render(request, "book_detail.html", {"book": book, "rate": [1, 2, 3, 4, 5], "form": CommentForm()})


class AddBook(View):
    def post(self, request):
        if request.user.is_authenticated:
            bf = BookForm(data = request.POST, files = request.FILES)
            book = bf.save(commit=True)
            book.authors.add(request.user)
            book.save()
        return redirect("the-main-page")


class AddComment(View):
    def post(self, request, slug):
        if request.user.is_authenticated:
            # Comment.objects.create(book_id=id, text=request.POST.get('text'), author_id=request.user.id)
            cf = CommentForm(data=request.POST)
            comment = cf.save(commit=False)
            comment.author_id = request.user.id
            comment.book_id = slug
            comment.save()
        return redirect("book-detail", slug=slug)


def comment_delete(request, id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=id)
        if request.user == comment.author:
            comment.delete()
    return redirect('book-detail', slug = comment.book.slug)


class UpdateComment(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=id)
            if request.user == comment.author:
                form = CommentForm(instance=comment)
                return render(request, "update_comment.html", {"form":form, "id":id})
        return redirect('book-detail', slug = comment.book.slug)

    def post(self, request, id):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=id)
            if request.user == comment.author:
                cf = CommentForm(instance=comment, data = request.POST)
                if cf.is_valid():
                    cf.save(commit=True)
        return redirect('book-detail', slug = comment.book.slug)



def book_delete(request, slug):
    if request.user.is_authenticated:
        book = Book.objects.get(slug=slug)
        if request.user in book.authors.all():
            book.delete()
    return redirect('the-main-page')


class UpdateBook(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            book = Book.objects.get(slug=slug)
            if request.user in book.authors.all():
                form = BookForm(instance=book)
                return render(request, "update_book.html", {"form":form, "slug":book.slug})
        return redirect('the-main-page')

    def post(self, request, slug):
        if request.user.is_authenticated:
            book = Book.objects.get(slug=slug)
            if request.user in book.authors.all():
                bf = BookForm(data = request.POST, files = request.FILES, instance=book)
                if bf.is_valid():
                    bf.save(commit=True)


        return redirect('the-main-page')






