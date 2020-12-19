from django.core.management.base import BaseCommand
from manager.models import Book, TMPBook
from slugify import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.all()

        instances = [
            TMPBook(
                title=b.title,
                date=b.date,
                text=b.text,
                count_rated_users=b.count_rated_users,
                count_all_stars=b.count_all_stars,
                rate=b.rate,
                slug=b.slug
            )
            for b in books
        ]

        TMPBook.objects.bulk_create(instances)
