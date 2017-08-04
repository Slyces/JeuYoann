from django import forms
from . import models


# =============================================================================
class UserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


# =============================================================================
class PlayerForm(forms.Form):
    name = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=models.genders)
