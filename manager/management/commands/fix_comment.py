from django.core.management.base import BaseCommand
from manager.models import Book, TMPBook, LikeBookUser, Comment
from slugify import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Book.objects.all().values("slug", "id")
        all_comments = Comment.objects.all()
        for book in query:
            comments = all_comments.filter(book_id=book["id"])
            for c in comments:
                c.tmp_book_id = book["slug"]

            Comment.objects.bulk_update(comments, ["tmp_book_id"])