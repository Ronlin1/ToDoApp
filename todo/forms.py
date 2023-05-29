from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from .models import Task
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(),
        validators=[EmailValidator(message='Please provide a valid email address')],
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    reminder_time = forms.IntegerField(min_value=0, label='Remind me (in minutes)')

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'reminder_time']