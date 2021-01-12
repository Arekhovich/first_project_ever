import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_shop.settings')

app = Celery()

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     "task_one": {
#         "task": "book_shop.tasks.update_repos",
#         "schedule": crontab(minute='3')
#     },
# }

app.autodiscover_tasks()

