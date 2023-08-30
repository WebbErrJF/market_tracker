from django.core.management.base import BaseCommand
from ...tasks import update_stock_db


class Command(BaseCommand):
    help = 'Runs the update_stock_db function for debugging'

    def handle(self, *args, **options):
        update_stock_db()
