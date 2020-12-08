from django.urls import path

from manager.views import hello, MyPage, AddLike, AddCommentLike

urlpatterns = [
    path('hello/', hello),
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path('add_like/<int:id>', AddLike.as_view(), name="add-like"),
    path('add_like_comment/<int:id>', AddCommentLike.as_view(), name="add-like-comment"),
    path("", MyPage.as_view(), name="the-main-page"),
]