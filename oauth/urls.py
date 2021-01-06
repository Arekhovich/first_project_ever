from django.urls import path, re_path

from oauth.views import GitOauth, GitCallback

urlpatterns = [
    re_path(r'^[-\w]+/', GitCallback.as_view(), name="the-git-callback"),
    path("", GitOauth.as_view(), name="the-git-page"),
]