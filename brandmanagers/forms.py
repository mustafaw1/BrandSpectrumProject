from django import forms
from .models import BrandManager

class BrandManagerForm(forms.ModelForm):
    class Meta:
        model = BrandManager
        fields = '__all__'