from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .choices import USER_TYPE_CHOICES
from brandmanagers.models import BrandManager

class InfluencerSignupForm(UserCreationForm):
    user_type = forms.CharField(max_length=15, required=True, widget=forms.Select(choices=USER_TYPE_CHOICES))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2')

class BrandManagerSignupForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=True)
    user_type = forms.CharField(max_length=15, required=True, widget=forms.Select(choices=USER_TYPE_CHOICES))



    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'password1', 'password2', 'company_name']


