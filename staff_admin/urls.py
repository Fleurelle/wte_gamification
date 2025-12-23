from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.staff_dashboard, name="staff-dashboard"),
    path("notifications/", views.staff_notifications, name="staff-notifications"),
]
