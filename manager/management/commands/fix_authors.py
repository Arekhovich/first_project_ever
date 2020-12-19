from django.core.management.base import BaseCommand
from manager.models import Book, TMPBook, LikeBookUser, Comment
from slugify import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Book.objects.all().values("slug", "id")
        all_lbu = LikeBookUser.objects.all()
        for book in query:
            new_set = all_lbu.filter(book_id=book["id"])
            for lbu in new_set:
                lbu.tmp_book_id = book['slug']
                lbu.save()
        LikeBookUser.objects.bulk_update(all_lbu, ["tmp_book_id"])