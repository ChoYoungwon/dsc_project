from __future__ import absolute_import, unicode_literals

# Celery를 import하여 앱이 항상 로드되도록 설정
from .celery import app as celery_app

__all__ = ('celery_app',)