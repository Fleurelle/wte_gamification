from django.urls import path

from .views import CommunityAttendanceView, SuccessView

urlpatterns = [
    path("community/", CommunityAttendanceView.as_view(), name="community"),
    path('success/', SuccessView.as_view(), name='success'),
]