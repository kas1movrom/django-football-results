from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Forecaster


@receiver(post_save, sender=User)
def create_forecaster_profile(sender, instance, created, **kwargs):
    if created:
        Forecaster.objects.create(
            user=instance, mail=instance.email, first_name=instance.first_name, last_name=instance.last_name
        )


@receiver(post_save, sender=Forecaster)
def send_notification(sender, instance, created, **kwargs):
    send_mail(
        "Notification from football service",
        f"Your forecaster profile was {'created' if created else 'updated'}",
        None,
        [instance.mail],
        fail_silently=False,
    )
