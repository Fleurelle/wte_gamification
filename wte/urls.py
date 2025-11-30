from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from user_accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user_accounts/", include("user_accounts.urls")),
    path('event_tracker/', include("event_tracker.urls")),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home")
]
