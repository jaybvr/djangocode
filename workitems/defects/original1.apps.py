from django.apps import AppConfig


class DefectsConfig(AppConfig):
    name = 'defects'
CELERY_IMPORTS = ('defects.tasks',)
