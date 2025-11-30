from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse

from django.shortcuts import render, redirect

from django.template.response import TemplateResponse

from django.urls import reverse_lazy

from django.utils.decorators import method_decorator

from django.views.generic.edit import FormView

from .forms import CommunityAttendanceForm


class CommunityAttendanceView(FormView):
    template_name = "attendance/community_event.html"
    form_class = CommunityAttendanceForm

    # def form_valid(self, form):
    #     form.register_attendance()
    #     return super().form_valid(form)

    @method_decorator(login_required)
    def get(self, request):
        context = {
            "form_data": f"{self.get_form()}"
        }
        # TODO: set attendee to logged in user 
        # TODO: disable attendee field editing
        # TODO ensure that admin is not in the assignee dropdown 
        # TODO ensure that the date field in the form_data is a date field, not a text field
        return TemplateResponse(request, self.template_name, context)

    # TODO: post method to submit the format
    @method_decorator(login_required)
    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            # Set the current user as attendee
            form.instance.attendee = request.user
            
            # Save the form
            form.save()
            
            # Redirect to success page
            return redirect(reverse_lazy("success!"))
        else:
            # Render the form again with error messages
            return TemplateResponse(request, self.template_name, {
                "form_data": form
            })
