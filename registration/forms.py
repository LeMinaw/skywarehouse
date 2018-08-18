from django import forms
from django.contrib.auth.forms import UserCreationForm
from warehouse.models import User

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['password1'].help_text = "At least 8 chars, not numeric, too common, or similar to personal information."
        self.fields['avatar']   .help_text = "Optionnal, you can change it later."
        self.fields['email']    .help_text = "Will be used for account activation."
       
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ["username", "email", "avatar", "password1", "password2"]
