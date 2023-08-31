from django.db import models
from accounts.models import CustomUser

from django.db import models

class InfluencerRegistration(models.Model):
    user_type = models.CharField(max_length=15, choices=CustomUser.USER_TYPE_CHOICES, default='brand_spectrum')
    # Basic Information
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other')
    profile_picture = models.ImageField(upload_to='profile_pics/')

    # Additional Details
    category = models.CharField(max_length=100)  # e.g., Sports, Music, Fitness
    marital_status = models.CharField(max_length=20, choices=[('single', 'Single'), ('married', 'Married'), ('other', 'Other')], default='single')
    children = models.PositiveIntegerField(default=0)  # Number of children
    children_ages = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of children's ages")

    def __str__(self):
        return self.name

    # Instagram Analytics
    # followers = models.PositiveIntegerField()
    # likes = models.PositiveIntegerField()
    # views = models.PositiveIntegerField()
    # engagements = models.PositiveIntegerField()
    # reach = models.PositiveIntegerField()
    # impressions = models.PositiveIntegerField()
    # growth_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.username



