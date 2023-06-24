from django.apps import AppConfig


class ApiFetcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_fetcher'

    def ready(self):
        from . import tasks_run
        tasks_run.start()
