from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Django 설정 모듈을 Celery에서 사용할 수 있도록 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# Celery 인스턴스 생성
app = Celery('main')

# Django의 settings.py에서 Celery 관련 설정을 가져온다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱에서 task를 자동으로 발견하도록 설정
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

