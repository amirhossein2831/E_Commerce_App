import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce.settings')

celery = Celery('e_commerce')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
