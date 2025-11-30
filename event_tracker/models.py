from django.conf import settings
from django.db import models

from django.urls import reverse


class Attendance(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_organizer = models.CharField(max_length=200)
    is_internal = models.BooleanField(default=False)

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