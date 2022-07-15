import os

from celery import Celery

from django.conf import settings




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'potluck.settings')

app = Celery('apps.send_notification')


app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
