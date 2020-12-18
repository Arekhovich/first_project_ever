from django.urls import path

from manager.views import hello, MyPage, AddCommentLike, BookDetail, AddRate2Book, AddBook, LoginView, \
    logout_user, AddComment

urlpatterns = [
    path('hello/', hello),
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path('add_like_comment/<str:slug>', AddCommentLike.as_view(), name="add-like-comment"),
    path('add_like_comment/<str:slug>/<str:location>/', AddCommentLike.as_view(), name="add-like-comment-location"),
    path("add_rate_to_book/<str:slug>/<int:rate>/", AddRate2Book.as_view(), name="add-rate"),
    path("add_rate_to_book/<str:slug>/<int:rate>/<str:location>/", AddRate2Book.as_view(), name="add-rate-location"),
    path("book_view_detail/<str:slug>/", BookDetail.as_view(), name="book-detail"),
    path("add_book/", AddBook.as_view(), name="add-book"),
    path("add_comment/<int:id>", AddComment.as_view(), name="add-comment"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("", MyPage.as_view(), name="the-main-page"),
]