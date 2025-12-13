from datetime import date
from django import forms
from django.contrib.auth.models import User
from .models import Attendance

class CommunityAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
        widgets = {
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-lg',
                'style': 'min-width: 400px;'
            }),
            # 'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    # def register_attendance(self):
    #     pass

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['attendee'].queryset = User.objects.filter(pk=user.pk)
            self.fields['attendee'].initial = user
            self.fields['attendee'].disabled = True

        # Customize field labels
        self.fields['event_name'].label = 'Event Name'
        self.fields['event_date'].label = 'Event Date'
        self.fields['event_organizer'].label = 'Event Organizer'
        # self.fields['is_internal'].label = 'Check this box if this a WTE hosted event'
        self.fields["activity_type"].label = "Activity Type"
        self.fields["proof_image"].label = "Upload Image"

    def clean_event_date(self):
        event_date = self.cleaned_data.get("event_date")
        if not event_date:
            return event_date

        today = date.today()
        # 1) Must be in the same year and month as today
        if event_date.year != today.year or event_date.month != today.month:
            raise forms.ValidationError(
                "You can only submit activities for the current month."
            )
        # 2) Must not be in the future
        if event_date > today:
            raise forms.ValidationError(
                "You cannot register attendance for a future date."
            )
        return event_date


# TODO:
# 2) This does not allow users to modify their entries (submitted events)
# 3) Anytime the is_internal button is clicked, users should receive 10 pts. Else, see event_tracker views

