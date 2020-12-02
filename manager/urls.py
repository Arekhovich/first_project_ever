from django.urls import path

from manager.views import hello, MyPage

urlpatterns = [
    path('hello/', hello),
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path("", MyPage.as_view(), name="the_main_page")
]