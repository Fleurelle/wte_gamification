from django.conf import settings
from django.db import models

from django.urls import reverse
from django.utils import timezone


class Attendance(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ("event_internal", "WTE Event"),
        ("event_external", "External Event"),
        ("social_media", "Social Media Engagement"),
        ("slack", "Slack Engagement"),
        ("sponsor_intro", "Sponsor Introduction"),
        ("mentorship", "Mentorship"),
        ("other", "Other"),
    ]

    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_organizer = models.CharField(max_length=200)
    # is_internal = models.BooleanField(default=False)

    activity_type = models.CharField(
        max_length=30,
        choices=ACTIVITY_TYPE_CHOICES,
        default="event_internal",
    )

    # simple proof: upload an image. TODO insert an optional description - FUTURE
    proof_image = models.ImageField(upload_to="activity_proofs/", blank=True, null=True)

    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attended_events",
        null=True
    )

    def get_absolute_url(self):
        return reverse("community")

    def __str__(self):
        return (
            f"Attendance {self.pk}: {self.attendee} attended "
            f"{self.event_name} on {self.event_date} organized by "
            f"{self.event_organizer}"
        )
    
# TODO UUID for usr account - this is because my user id in the url is only a single digit