from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, IntegerField
from django.shortcuts import render, redirect
from django.utils import timezone
from event_tracker.models import Attendance, Notification
import calendar
import pytz

# staff_admin/views.py

@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect("home")
    
    eastern_tz = pytz.timezone("America/New_York")
    today = timezone.now().astimezone(eastern_tz).date()

    this_year = today.year
    this_month = calendar.month_name[today.month]
    
    # Which mode? default = this_month
    mode = request.GET.get("mode", "this_month")

    if mode == "all_time":
        events_qs = Attendance.objects.all()
    elif mode == "this_year":
        events_qs = Attendance.objects.filter(
            event_date__year=today.year,
        )
    else:
        events_qs = Attendance.objects.filter(
            event_date__year=today.year,
            event_date__month=today.month,
        )

    has_attendance = events_qs.exists()

    # Top users by total rewards
    top_users = (
        events_qs
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

    context = {
        "top_users": top_users,
        "notifications": notifications,
        "unread_count": unread_count,
        "has_attendance": has_attendance,
        "mode": mode,
        "this_year": this_year,
        "this_month": this_month,
    }
    return render(request, "dashboard/staff-dashboard.html", context)

@login_required
def staff_notifications(request):
    if not request.user.is_staff:
        return redirect("home")
    
    notifications = Notification.objects.select_related("user").order_by("-created_at")
    
    # Mark individual notification as read
    if request.method == "POST" and 'notification_id' in request.POST:
        notification_id = request.POST['notification_id']
        Notification.objects.filter(id=notification_id, is_read=False).update(is_read=True)

    # Mark ALL as read
    if request.method == "POST" and request.POST.get('mark_all'):
        Notification.objects.filter(is_read=False).update(is_read=True)

    context = {
        "notifications": notifications,
    }
    return render(request, "dashboard/staff-notifications.html", context)


# TODO:
# Mark individual notifications as read
# clear notifications - staff-notifications/ page, not on the dashboard.
# Give 10 points for account creation


