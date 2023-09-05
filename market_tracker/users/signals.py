from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, SubscribedCompanies
from api_fetcher.models import StockCompany
from django.utils import timezone


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        default_companies = StockCompany.objects.filter(Default=True)
        for count, default_company in enumerate(default_companies, start=1):
            SubscribedCompanies.objects.create(user=instance, stock_company=default_company, dashboard_number=count,
                                               subscription_date=timezone.now())
