from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make all fields required
        for field in ('first_name', 'last_name', 'username', 'password'):
            self.fields[field].required = True
            
        # Customize field labels
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'