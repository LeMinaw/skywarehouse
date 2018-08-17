from django import forms
from django.contrib.auth.forms import UserCreationForm
from warehouse.models import *

class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "avatar", "password1", "password2"]
