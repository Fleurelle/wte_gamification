from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, IntegerField
from django.shortcuts import render, redirect
from django.utils import timezone
from event_tracker.models import Attendance, Notification
import pytz

# staff_admin/views.py

@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect("home")

    # Top users by total rewards
    top_users = (
        Attendance.objects
        .values("attendee__id", "attendee__first_name", "attendee__last_name")
        .annotate(
            total_points=Sum(
                Case(
                    When(activity_type="event_external", then=8),
                    default=10,
                    output_field=IntegerField(),
                )
            )
        )
        .order_by("-total_points")
    )

    # Latest notifications
    notifications = (
        Notification.objects
        .select_related("user")
        .order_by("-created_at")[:20]
    )

    unread_count = Notification.objects.filter(is_read=False).count()
    print("DEBUG unread_count =", unread_count)

    # Check if there is any attendance this month (Eastern)
    eastern_tz = pytz.timezone("America/New_York")
    today = timezone.now().astimezone(eastern_tz).date()

    events_this_month = Attendance.objects.filter(
        event_date__year=today.year,
        event_date__month=today.month,
    )

    has_attendance_this_month = events_this_month.exists()

    context = {
        "top_users": top_users,
        "notifications": notifications,
        "unread_count": unread_count,
        "has_attendance_this_month": has_attendance_this_month,
    }
    return render(request, "dashboard/staff-dashboard.html", context)

@login_required
def staff_notifications(request):
    if not request.user.is_staff:
        return redirect("home")

    notifications = Notification.objects.select_related("user").order_by("-created_at")

    # mark as read
    if request.method == "POST":
        notifications.filter(is_read=False).update(is_read=True)
        return redirect("staff-notifications")

    context = {
        "notifications": notifications,
    }
    return render(request, "dashboard/staff-notifications.html", context)


# TODO:
# Mark notifications as read
# clear notifications - staff-notifications/ page, not on the dashboard. 
# timezone for notifications


