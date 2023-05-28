from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from .models import Task

class CustomUserCreationForm(UserCreationForm):
    # email = forms.EmailField(
    #     max_length=254,
    #     required=True,
    #     widget=forms.EmailInput(),
    #     validators=[EmailValidator(message='Please provide a valid email address')]
    # )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Add your custom password strength validation logic here
        if len(password1) < 8:
            raise forms.ValidationError('Password should be at least 8 characters long.')

        # Call the parent's clean_password2 method to perform the default validation
        return super().clean_password2()
    
# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         exclude = ('created', )


# class ReminderForm(forms.Form):
#     reminder_time = forms.IntegerField(label='Reminder (in minutes):', min_value=1, max_value=60)


from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    reminder_time = forms.IntegerField(min_value=0, label='Remind me (in minutes)')

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'reminder_time']