from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_analysis_ids.settings')

app = Celery('network_analysis_ids')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'
app.autodiscover_tasks()