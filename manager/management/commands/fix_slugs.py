from django.core.management.base import BaseCommand
from manager.models import Book
from slugify import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.all()
        for b in books:
            b.slug = slugify(b.title)
            try:
                b.save()
            except:
                b.slug += str(b.id)
                b.save()