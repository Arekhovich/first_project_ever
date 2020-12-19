from django.core.management.base import BaseCommand
from manager.models import Book, TMPBook, LikeBookUser, Comment
from slugify import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.all()
        tmp_books = TMPBook.objects.all()
        for book in books:
            tmp_book = tmp_books.get(slug=book.slug)
            for author in book.authors.all():
                tmp_book.authors.add(author)
            tmp_book.save()