from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import requests
import webbrowser
import base64

from manager.models import Profile

client_id = '337aad28ea23eaed3ddd'
client_secret = 'e6f94809cc64336ab6ff5bcf02b213ffa3adc133'
redirect_url = 'http://localhost:8000/oauth/callback'


class GitOauth(View):
    def get(self, request):

        url = "https://github.com/login/oauth/authorize?client_id={GIT_CLIENT_ID}"
        return render(request, 'git.html', {'url': url})

class GitCallback(View):
    def get(self, request):
        code = request.GET.get("code", "")
        url = 'https://github.com/login/oauth/access_token'
        data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
        token = requests.post(url, data=data).text
        token = token[13:-25]
        #Profile.objects.get(user=request.user).git_token = token
        user=request.user
        connections_url = 'https://api.github.com/user'
        response = requests.get(connections_url,
                                headers={'Authorization': 'token  ' + token})
        login= response.json()['login']
        repos = requests.get("https://api.github.com/users/" + login + "/repos").json()
        repos_list = []
        for r in repos:
            repos_list.append(r['name'])

        output = "{0}{1}".format(repos_list, user)
        return HttpResponse(output)
