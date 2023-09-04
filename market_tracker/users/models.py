from django.db import models
from django.contrib.auth.models import User
from api_fetcher.models import StockCompany
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.avif', upload_to='profile_pics/')
    description = models.TextField(help_text='Describe yourself in few words')

    def __str__(self):
        return str(self.user.username)


class SubscribedCompanies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_company = models.ForeignKey(StockCompany, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(null=True)
    dashboard_number = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])

    class Meta:
        unique_together = ('user', 'stock_company')

    def clean(self):
        if 1 <= self.dashboard_number <= 4:
            queryset = SubscribedCompanies.objects.filter(
                user=self.user,
                dashboard_number=self.dashboard_number
            )
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            if queryset.exists():
                raise ValidationError({'dashboard_number': 'This number is already taken.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)