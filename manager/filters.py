import django_filters

from manager.models import Book


class GenreFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['genre']

