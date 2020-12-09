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
    likes = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField(User, through="manager.LikeBookUser", related_name="liked_books")


    def __str__(self):
        return f"{self.title}{self.id: >50}"

class LikeBookUser(models.Model):
    class Meta:
        unique_together = ("user", "book")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_book_table")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="liked_user_table")

    # def save(self, **kwargs):
    #     try:
    #         super().save(**kwargs)
    #     except:
    #         LikeBookUser.objects.get(user=self.user,book=self.book).delete()

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeBookUser.objects.get(user=self.user, book=self.book).delete()
            self.book.likes -= 1
        else:
            self.book.likes += 1
        self.book.save()


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    likes_com = models.ManyToManyField(User, through="manager.LikeComment", related_name="liked_comments")

class LikeComment(models.Model):
    class Meta:
        unique_together = ("user", "comment") #взаимоуникальные поля
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_comment_table")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_comm_user_table")

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeComment.objects.get(user=self.user,comment=self.comment).delete()

# Create your models here.
