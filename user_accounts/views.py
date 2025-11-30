from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_invalid(self, form):

        # Get the form data
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        
        # Try to authenticate the user
        user = authenticate(self.request, username=username, password=password)
        
        # Check if both fields are empty
        if not username and not password:
            messages.error(self.request, 'Please enter both username and password.')
        # Check if username is empty
        elif not username:
            messages.error(self.request, 'Please enter your username.')
        # Check if password is empty
        elif not password:
            messages.error(self.request, 'Please enter your password.')
        # If credentials were provided but invalid
            # TODO: automatically send the user to the signup page if an account is not found
        elif user is None:
            # Check if user exists in database
            try:
                user_obj = User.objects.get(username=username)
                messages.error(self.request, 'Invalid username or password. Please try again.')
                # TODO in the error message for existing username, be sure to include the incorrect entered username for reference. 
                # TODO if username exists, send user to log in page
            except User.DoesNotExist:
                messages.error(self.request, 'Account not found. Please click the Sign Up button below.')
        # If authentication failed for other reasons
        else:
            messages.error(self.request, 'Authentication failed. Please try again.')
            
        return super().form_invalid(form)