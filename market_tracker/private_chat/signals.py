from django.db.models.signals import post_save
from .models import UserContact
from django.dispatch import receiver


@receiver(post_save, sender=UserContact)
def create_profile(sender, instance, created, **kwargs):
    if created:
        existing_contact = UserContact.objects.filter( user=instance.contact, contact=instance.user).exists()
        if not existing_contact:
            UserContact.objects.create(user=instance.contact, contact=instance.user)
