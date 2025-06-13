from django import forms
from .models import Vehicle
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['owner_name', 'vehicle_type', 'number_plate']

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

