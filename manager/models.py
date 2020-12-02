from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='ну это типа имя книги'
    )
    date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField(max_length=200, null=True)
    authors = models.ManyToManyField(User, related_name="books")


    def __str__(self):
        return f"{self.title}{self.id: >50}"


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

# Create your models here.
