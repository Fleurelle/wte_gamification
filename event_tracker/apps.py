from django.apps import AppConfig


class EventTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event_tracker'

    def ready(self):
        import event_tracker.signals
