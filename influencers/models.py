from django.contrib.auth import get_user_model
from django.db import models
from accounts.choices import USER_TYPE_CHOICES
from campaigns.models import Campaign  # Import your Campaign model

class InfluencerRegistration(models.Model):
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='brand_spectrum')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other')
    profile_picture = models.ImageField(upload_to='profile_pics/')
    
    # Additional Details
    category = models.CharField(max_length=100)  # e.g., Sports, Music, Fitness
    marital_status = models.CharField(max_length=20, choices=[('single', 'Single'), ('married', 'Married'), ('other', 'Other')], default='single')
    children = models.PositiveIntegerField(default=0)  # Number of children
    children_ages = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of children's ages")
    
    campaigns = models.ManyToManyField(Campaign, related_name='influencers', blank=True)
    
    # Create a foreign key to your custom user model
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='influencer_registration', null=True, blank=True)

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
    def get_campaigns(self):
        return self.campaigns.all()



