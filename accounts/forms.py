from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .choices import USER_TYPE_CHOICES

class InfluencerSignupForm(UserCreationForm):
    user_type = forms.CharField(max_length=15, required=True, widget=forms.Select(choices=USER_TYPE_CHOICES))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2')
