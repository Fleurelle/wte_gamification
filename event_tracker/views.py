from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse

from django.shortcuts import render, redirect

from django.template.response import TemplateResponse

from django.urls import reverse_lazy

from django.utils import timezone

from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from django.views.generic.edit import FormView

from .forms import CommunityAttendanceForm

from .models import Attendance

import pytz

# Successful event submission view
class SuccessView(TemplateView):
    template_name = "success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_attendance = Attendance.objects.filter(
            attendee=self.request.user
        ).order_by('-id')[:1].first()
        
        if last_attendance:
            context['message'] = f"Thank you for registering your attendance to {last_attendance.event_name}!"
        else:
            context['message'] = "Thank you for registering your attendance!"
            
        return context

class CommunityAttendanceView(FormView):
    template_name = "attendance/community_event.html"
    form_class = CommunityAttendanceForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass the logged-in user
        return kwargs

    @method_decorator(login_required)
    def get(self, request):
        form = self.get_form()
        context = {
            "form_data": form
        }

        return TemplateResponse(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        # form = self.get_form()
        form = self.form_class(
            data=request.POST,
            files=request.FILES,
            user=request.user,
    )
        if form.is_valid():
            # # Set the current user as attendee
            # form.instance.attendee = request.user
            
            # # Save the form
            # form.save()

            attendance = form.save(commit=False)
            attendance.attendee = request.user

            attendance.save()

            # derive points from activity_type
            activity_type = attendance.activity_type
            if activity_type == "event_external":
                earned_points = 8
            else:
                earned_points = 10
            
            # Redirect to success page
            return redirect(reverse_lazy("success"))
        else:
            # Render the form again with error messages
            return TemplateResponse(request, self.template_name, {
                "form_data": form
            })


class HomeView(TemplateView):
    template_name = "home.html"

    @method_decorator(login_required)    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Total # of events attended
        user_events = Attendance.objects.filter(
            attendee=self.request.user)
        
        total_events_attended = user_events.count()

        # Rewards earned to date (of all time)
        rewards_to_date = 0
        for event in user_events:
            rewards_to_date += 8 if event.activity_type == 'event_external' else 10

        # Rewards earned this month
        eastern_tz = pytz.timezone("America/New_York")
        today = timezone.now().astimezone(eastern_tz)
        events_this_month = user_events.filter(
            event_date__year=today.year,
            event_date__month=today.month,
        )
        rewards_this_month = 0
        for event in events_this_month:
            rewards_this_month += 8 if event.activity_type == 'event_external' else 10

        context = {
            'total_events_attended': total_events_attended,
            'rewards_to_date': rewards_to_date,
            'rewards_this_month': rewards_this_month,
        }

        return self.render_to_response(context)
    

# TODO - 
#     internal events == 10 pts
#     community events == 8 pts
#     slack discussions/post == 5 pts
#     referrals == 6 pts
#     joining the board == 12 pts
# MAYBE - the form should change depending on the activity type