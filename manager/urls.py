from django.urls import path, re_path
from django.views.decorators.cache import cache_page


from manager.views import MyPage, AddCommentLike, BookDetail, AddRate2Book, AddBook, LoginView, \
    logout_user, AddComment, book_delete, UpdateBook, comment_delete, UpdateComment, RegisterView, \
    PageGenre, update_profile, GitReposCallback
from manager.views_ajax import add_rate, delete_book, add_comment_ajax, DeleteComment, AddLikeComment, CreateBook

urlpatterns = [
    path('add_like_comment/<int:id>', AddCommentLike.as_view(), name="add-like-comment"),
    path('add_like_comment/<int:id>/<str:location>/', AddCommentLike.as_view(), name="add-like-comment-location"),
    path("add_rate_to_book/<str:slug>/<int:rate>/", AddRate2Book.as_view(), name="add-rate"),
    path("add_rate_to_book/<str:slug>/<int:rate>/<str:location>/", AddRate2Book.as_view(), name="add-rate-location"),
    path("add_rate_ajax", add_rate),
    path("book_view_detail/<str:slug>/", BookDetail.as_view(), name="book-detail"),
    path("add_book/", AddBook.as_view(), name="add-book"),
    path("add_comment/<str:slug>/", AddComment.as_view(), name="add-comment"),
    path("delete_book/<str:slug>/", book_delete, name="delete-book"),
    path("update_book/<str:slug>/", UpdateBook.as_view(), name="update-book"),
    path("delete_comment/<int:id>/", comment_delete, name="delete-comment"),
    path("update_comment/<int:id>/", UpdateComment.as_view(), name="update-comment"),
    path('page_genre/<str:genre>/', PageGenre.as_view(), name="page-genre"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout_user, name="logout"),
    path("account/", update_profile, name="account"),
    path('add_like2comment_ajax/<int:pk>', AddLikeComment.as_view()),
    path('add_comment_ajax', add_comment_ajax, name='comment-ajax'),
    path('delete_comment_ajax/<int:pk>', DeleteComment.as_view()),
    path('delete_book_ajax', delete_book),
    path('create_book_ajax', CreateBook.as_view()),
    re_path(r'^[-\w]+/', GitReposCallback.as_view(), name="the-git-repos"),
    path("", MyPage.as_view(), name="the-main-page"),
]
