import requests
from django.contrib.auth.models import User
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
    requests.post(
        url="http://127.0.0.1:8001/events",
        json={
            "type": f"profile_{'created' if created else 'updated'}",
            "user": {
                "external_id": instance.id,
                "email": f"{instance.mail}",
                "role": f"{'admin' if instance.admin else 'user'}",
            },
            "payload": {"greeting": "Hello", "user": f"{instance.first_name}"},
        },
    )
