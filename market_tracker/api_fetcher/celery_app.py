import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "market_tracker.settings")
django.setup()

from celery import Celery
from .tasks import update_stock_db

scheduler = {"time_scheduler": {"task": "api_fetcher.celery_app.process_data", "schedule": 30.0}}
celery_obj = Celery("api_fetcher", broker="redis://redis:6379/0", backend="redis://redis:6379/0", beat_schedule=scheduler)

celery_obj.autodiscover_tasks()


@celery_obj.task()
def process_data():
    update_stock_db()