from django import forms
from django.contrib.auth.models import User
from .models import Attendance

class CommunityAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
    
    def register_attendance(self):
        pass

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['attendee'].queryset = User.objects.all()

# TODO: This does not allow users to modify their entries (submitted events)
