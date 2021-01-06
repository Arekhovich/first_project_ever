from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

import requests
import webbrowser
import base64

client_id = '337aad28ea23eaed3ddd'
client_secret = 'e6f94809cc64336ab6ff5bcf02b213ffa3adc133'
redirect_url = 'http://localhost:8000/oauth/callback'


class GitOauth(View):
    def get(self, request):
        client_id = '337aad28ea23eaed3ddd'
        auth_url = ('''https://github.com/login/oauth/authorize''' +
                    '''?client_id=''' + client_id +
                    '''&redirect_uri=http://localhost:8000/oauth/callback''')
        return render(request, 'git.html')

class GitCallback(View):
    def get(self, request):
        code = request.GET.get("code", "")
        url = 'https://github.com/login/oauth/access_token'
        data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
        token = requests.post(url, data=data).text
        token = token[13:-25]
        connections_url = 'https://api.github.com/user'
        response = requests.get(connections_url,
                                headers={'Authorization': 'token  ' + token})
        login= response.json()['login']
        repos = requests.get("https://api.github.com/users/" + login + "/repos").json()
        repos_list = []
        for r in repos:
            repos_list.append(r['name'])

        output = "{0}".format(repos_list)
        return HttpResponse(output)
