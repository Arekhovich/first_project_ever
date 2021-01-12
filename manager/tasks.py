from time import sleep
import requests
from celery import shared_task
from manager.models import GitRepos, GitToken

from manager.models import GitRepos


@shared_task()
def update_repos():
    tokens = GitToken.objects.all()
    connections_url = 'https://api.github.com/user'
    for t in tokens:
        response = requests.get(connections_url,
                                headers={'Authorization': 'token  ' + t.git_token})
        login = response.json()['login']
        repos = requests.get("https://api.github.com/users/" + login + "/repos").json()
        user_id = t.user_id
        if GitRepos.objects.filter(user_id=user_id):
            GitRepos.objects.filter(user_id=user_id).delete()
            for r in repos:
                GitRepos.objects.create(user_id=user_id, title_repos=r['name'])
        else:
            for r in repos:
                GitRepos.objects.create(user_id=user_id, title_repos=r['name'])
