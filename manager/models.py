from json import loads, dumps

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from slugify import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class Genre(models.Model):
    name_genre = models.TextField()

    def __str__(self):
        return self.name_genre


class Book(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='ну это типа имя книги'
    )
    date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField(max_length=2000, null=True, verbose_name='Описание')
    authors = models.ManyToManyField(User, related_name="books")
    rate = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    count_rated_users = models.PositiveIntegerField(default=0)
    count_all_stars = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField(User, through="manager.LikeBookUser", related_name="liked_books")
    slug = models.SlugField(primary_key=True)
    genre = models.ManyToManyField(Genre, null=True, blank=True, related_name='genre_of_book', verbose_name='Жанр')
    cover = models.ImageField('Обложка', upload_to="manager/", null=True, blank=True)

    def __str__(self):
        return f"{self.title}{self.slug:}"

    def save(self, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.title)
        try:
            super().save(**kwargs)
        except:
            self.slug += str(self.date)
            super().save(**kwargs)


class LikeBookUser(models.Model):
    class Meta:
        unique_together = ("user", "book")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_book_table")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="liked_user_table", null=True)
    rate = models.PositiveIntegerField(default=5)

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            lbu = LikeBookUser.objects.get(user=self.user, book=self.book)
            self.book.count_all_stars -= lbu.rate
            lbu.rate = self.rate
            lbu.save()
        else:
            self.book.count_rated_users += 1
        self.book.count_all_stars += self.rate
        self.book.rate = self.book.count_all_stars / self.book.count_rated_users
        self.book.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    about_user = models.TextField(max_length=300, null=True, blank=True, verbose_name='О себе')
    photo = models.ImageField(upload_to='manager/', blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class VisitPage(models.Model):
    class Meta:
        unique_together = ("user", "book")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visit_user")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="visit_book")

    def __str__(self):
        return f"{self.book}"

    def save(self, **kwargs):
        super().save(**kwargs)


class GitAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="repos_user")
    github_account = models.CharField(null=True, max_length=100)
    _title_repos = models.TextField(null=True)

    @property
    def title_repos(self):
        if self._title_repos is not None:
            return loads(self._title_repos)
        return []

    @title_repos.setter
    def title_repos(self, value):
        assert isinstance(value, list), "you can set"
        self._title_repos = dumps(value)


class Comment(models.Model):
    text = models.TextField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments", null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    likes_com = models.ManyToManyField(User, through="manager.LikeComment", related_name="liked_comments")


class LikeComment(models.Model):
    class Meta:
        unique_together = ("user", "comment")  # взаимоуникальные поля
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_comment_table")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_comm_user_table")

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeComment.objects.get(user=self.user, comment=self.comment).delete()
            self.comment.likes -= 1
        else:
            self.comment.likes += 1
        self.comment.save()
