# event_tracker/signals.py
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification

User = get_user_model()


@receiver(post_save, sender=User)
def create_signup_notification(sender, instance, created, **kwargs):
    if not created:
        return

    Notification.objects.create(
        type="signup",
        user=instance,
        message=(
            f"New account created: "
            f"{instance.get_full_name()}"
        ),
    )
