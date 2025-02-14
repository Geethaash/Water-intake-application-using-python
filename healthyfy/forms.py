from django import forms
from .models import intakeEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WaterintakeForm(forms.ModelForm):
    class Meta:
        model = intakeEntry
        fields = ['intake'] 


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text  = None





