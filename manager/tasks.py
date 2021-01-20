from time import sleep
import requests
from celery import shared_task
from manager.models import GitAccount


@shared_task()
def update_repos():
    logins = GitAccount.objects.all()
    for log in logins:
        response_repos = requests.get("https://api.github.com/users/" + log.github_account + "/repos").json()
        repos = [r['name'] for r in response_repos]
        user_id = log.user_id
        GitAccount.objects.filter(user_id=user_id).delete()
        GitAccount.objects.create(user_id=user_id, github_account=log.github_account, _title_repos=repos)


