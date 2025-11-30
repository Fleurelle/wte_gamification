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
            })
        }
    
    def register_attendance(self):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required
        for field in self.fields.values():
            field.required = True
        # Customize field labels
        self.fields['event_name'].label = 'Event Name'
        self.fields['event_date'].label = 'Event Date'
        self.fields['event_organizer'].label = 'Event Organizer'
        self.fields['is_internal'].label = 'Internal Event'

# TODO:
# 1) date field to be an actual date field, not text - DONE
# 2) This does not allow users to modify their entries (submitted events)
# 3) ensure that the attendee field is already auto populated in the form
