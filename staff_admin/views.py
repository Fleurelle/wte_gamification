from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, IntegerField
from django.shortcuts import render, redirect
from event_tracker.models import Attendance, Notification

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
        .order_by("-total_points")[:10]
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
    }
    return render(request, "dashboard/staff-dashboard.html", context)

# staff_admin/views.py

@login_required
def staff_notifications(request):
    if not request.user.is_staff:
        return redirect("home")

    notifications = Notification.objects.select_related("user").order_by("-created_at")

    # mark all as read when visiting
    if request.method == "POST":
        notifications.filter(is_read=False).update(is_read=True)
        return redirect("staff-notifications")

    context = {
        "notifications": notifications,
    }
    return render(request, "dashboard/staff-notifications.html", context)




