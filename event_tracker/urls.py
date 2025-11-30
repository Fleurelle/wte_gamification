from django.urls import path

from .views import CommunityAttendanceView

urlpatterns = [
    path("community/", CommunityAttendanceView.as_view(), name="community"),
]