from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from user_accounts import views as uav
from event_tracker import views as etv


urlpatterns = [
    path('admin/', admin.site.urls),
    path("user_accounts/", include("user_accounts.urls")),
    path('event_tracker/', include("event_tracker.urls")),
    path('accounts/login/', uav.CustomLoginView.as_view(), name='login'),
    path("accounts/logout/", uav.logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("", TemplateView.as_view(template_name="home.html"), name="home")
    # path("", etv.HomeView.as_view(), name="home"),
    path("", etv.home_router, name="home"),
    path("staff/", include("staff_admin.urls")),    
    path('feedback/', uav.submit_feedback, name='submit_feedback'),
]