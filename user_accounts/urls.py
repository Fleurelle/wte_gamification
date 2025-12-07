from django.urls import path

from .views import SignUpView, user_profile


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/<int:pk>/", user_profile, name="user-profile")
]