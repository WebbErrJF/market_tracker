from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import update_stock_db


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_stock_db, 'interval', seconds=300)
    scheduler.start()
