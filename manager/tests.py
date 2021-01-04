from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase, Client
from slugify import slugify

from manager.forms import CustomAuthenticationForm
from manager.models import Book, Comment


class TestMyAppPlease(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='katerina', password='katerina1992')
        self.client = Client()
        self.user1 = User.objects.create_user('test_name1')
        self.user2 = User.objects.create_user('test_name2')

    def test_add_book(self):
        self.client.force_login(self.user1)
        url = reverse('add-book')
        data = {
            'title': 'test title',
            'text': 'test-text'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg = 'not redirect ')
        self.assertTrue(Book.objects.exists(), msg = 'book is not created')
        book = Book.objects.first()
        self.assertEqual(book.title, data['title'])
        self.assertEqual(book.slug, slugify(data['title']))
        self.assertEqual(book.text, slugify(data['text']))
        self.assertEqual(book.authors.first(), self.user1)
        self.client.logout()
        data = {
            'title': 'test title',
            'text': 'test-text'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='not redirect ')
        self.assertEqual(Book.objects.count(), 1,  msg='book without author')

    def test_update_book(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title = 'test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        self.book2 = Book.objects.create(title = 'test_title2')
        self.assertEqual(Book.objects.count(), 2)
        data = {
            'title': 'test-title2',
            'text': 'test-text'
        }
        url = reverse('update-book', kwargs=dict(slug=self.book1.slug))
        response = self.client.post(url, data)
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book1.title, data['title'], msg='book1 is not refresh')
        self.assertEqual(self.book1.text, data['text'], msg = 'book is not refresh')
        self.assertEqual(self.book1.authors.first(), self.user)
        self.client.logout()
        url = reverse('update-book', kwargs=dict(slug=self.book1.slug))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.book2.refresh_from_db()
        self.assertNotEqual(self.book2.title, data['title'])
        self.assertNotEqual(self.book2.text, data['text'])

    def test_update_book_get(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title = 'test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('update-book', kwargs=dict(slug=self.book1.slug))
        response = self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        # не аутентифицирован
        self.client.logout()
        url = reverse('update-book', kwargs=dict(slug=self.book1.slug))
        response = self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, 302)

    def test_rate_book(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=3))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 3)
        #new user
        self.client.force_login(self.user1)
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=4))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 3.5)
        # new user
        self.client.force_login(self.user2)
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=5))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 4)

    def test_book_delete(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        self.book2 = Book.objects.create(title='test_title2')
        self.assertEqual(Book.objects.count(), 2)
        url = reverse('delete-book', kwargs=dict(slug=self.book1.slug))
        self.client.get(url)
        self.assertEqual(Book.objects.count(), 1)
        url = reverse('delete-book', kwargs=dict(slug=self.book2.slug))
        self.client.get(url)
        self.assertEqual(Book.objects.count(), 1)
        self.client.logout()
        self.client.get(url)
        self.assertEqual(Book.objects.count(), 1)

    def test_like_comment(self):
        self.client.force_login(self.user)
        self.comment = Comment.objects.create(text='5+')
        url = reverse('add-like-comment', kwargs=dict(id=self.comment.id))
        self.client.get(url)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.likes, 1)
        # follow user
        self.client.force_login(self.user1)
        url = reverse('add-like-comment', kwargs=dict(id=self.comment.id))
        self.client.get(url)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.likes, 2)


    def test_main_page(self):
        login = self.client.login(username='username', password='password')
        resp = self.client.get(reverse('the-main-page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_login(self):
        url = reverse('login')
        data = {
            'username': 'katerina',
            'password': 'katerina1992'
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.exists(), msg='User is not exist')
        data2 = {
            'username': 'katerina',
            'password': 'katrina199'
        }
        response = self.client.post(url, data2)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.exists(), msg='User is not exist')

    def test_logout(self):
        self.client.force_login(self.user)
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.exists())

    def test_registration(self):
        url = reverse('register')
        data = {
            'username': 'kate',
            'password1': '5544kate',
            'password2': '5544kate'
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.exists(), msg='User is not exist')

    def test_registration_error(self):
        url = reverse('register')
        data = {
            'username': 'kate',
            'password1': 'kate344',
            'password2': '344'
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.exists(), msg='User is not exist')

    def test_book_detail(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('book-detail', kwargs=dict(slug=self.book1.slug))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')

    def test_add_comment(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        response = self.client.post(url, data={'text': 'test comment'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_delete_comment(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        response = self.client.post(url, data={'text': 'test comment'})
        id = Comment.objects.first().id
        url = reverse('delete-comment', kwargs=dict(id=id))
        response = self.client.get(url)
        self.assertEqual(Comment.objects.count(), 0)

    def test_update_comment(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        response = self.client.post(url, data={'text': 'test comment'})
        id = Comment.objects.first().id
        url = reverse('update-comment', kwargs=dict(id=id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        response = self.client.post(url, data={'text': "new text"})
        self.assertEqual(response.status_code, 302)



    def test_genre(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        url = reverse('page-genre', kwargs=dict(genre=self.book1.genre))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'page_books_genre.html')








class TestMyAppExcepts(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_name')
        self.user1 = User.objects.create_user('test_name1')
        self.user2 = User.objects.create_user('test_name2')


    def test_rate_repeat(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title='test_title1')
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=3))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 3)
        #repeat user
        self.client.force_login(self.user)
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=4))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 4)
        # new user
        self.client.force_login(self.user2)
        url = reverse('add-rate', kwargs=dict(slug=self.book1.slug, rate=2))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 3)

    def test_like_comment_except(self):
        self.client.force_login(self.user)
        self.comment = Comment.objects.create(text='5+')
        url = reverse('add-like-comment', kwargs=dict(id=self.comment.id))
        self.client.get(url)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.likes, 1)
        # repeat user
        self.client.force_login(self.user)
        url = reverse('add-like-comment', kwargs=dict(id=self.comment.id))
        self.client.get(url)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.likes, 0)

    def test_except_slug(self):
        self.client.force_login(self.user)
        self.book1 = Book.objects.create(title = 'test_title1')
        self.book1.authors.add(self.user)
        self.book1.save()
        data = {
            'title': 'test_title2',
            'text': 'test_text'
        }
        url = reverse('update-book', kwargs=dict(slug=self.book1.slug))
        response = self.client.post(url, data)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, data['title'], msg='book1 is not refresh')
        self.assertEqual(self.book1.text, data['text'], msg = 'book is not refresh')
        self.book2 = Book.objects.create(title='test_title1')
        self.assertNotEqual(self.book2.slug, 'test-title1')








