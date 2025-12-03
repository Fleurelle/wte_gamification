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
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
        self.fields['is_internal'].label = 'Check this box if this a WTE hosted event'



# TODO:
# 1) date field to be an actual date field, not text - DONE
# 2) This does not allow users to modify their entries (submitted events)
# 3) ensure that the attendee field is already auto populated in the form
# 4) the internal event dropdown in the form is disabled on the frontend 
    # a) Enable form
    # b) Ensure tht form is a dropdown

