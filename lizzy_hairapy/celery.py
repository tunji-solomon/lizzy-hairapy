import os
import platform
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lizzy_hairapy.settings')
app = Celery('lizzy_hairapy')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

