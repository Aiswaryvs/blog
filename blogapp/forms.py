from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from blogapp.models import UserProfile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "first_name","last_name","username","email","password1","password2"
        ]


class LoginForm(forms.Form):
        username=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
        password=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))


class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user",)
        widgets={
            "date_of_birth":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

