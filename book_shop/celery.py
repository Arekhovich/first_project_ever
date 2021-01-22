import os

from celery import Celery

from django.conf import settings

if settings.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_shop.settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_shop.settingsPROD')

app = Celery()

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

