from django.urls import path

from manager.views import hello, MyPage, AddCommentLike, BookDetail, AddRate2Book

urlpatterns = [
    path('hello/', hello),
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path('add_like_comment/<int:id>', AddCommentLike.as_view(), name="add-like-comment"),
    path('add_like_comment/<int:id>/<str:location>/', AddCommentLike.as_view(), name="add-like-comment-location"),
    path("add_rate_to_book/<int:id>/<int:rate>/", AddRate2Book.as_view(), name="add-rate"),
    path("add_rate_to_book/<int:id>/<int:rate>/<str:location>/", AddRate2Book.as_view(), name="add-rate-location"),
    path("book_view_detail/<int:id>/", BookDetail.as_view(), name="book-detail"),
    path("", MyPage.as_view(), name="the-main-page"),
]