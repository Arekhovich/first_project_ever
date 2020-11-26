from django.urls import path

from manager.views import hello, buybook

urlpatterns = [
    path('hello/', hello),
    path('shop/buybook/', buybook)
]