from django.utils import timezone
from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from accounts.choices import USER_TYPE_CHOICES


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='campaign_images/') 
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='Influencer') 
    is_public = models.BooleanField(default=False)

    influencers = models.ManyToManyField(get_user_model(), related_name='campaigns', blank=True)
    media_type = models.CharField(max_length=20, default=None)  # e.g., 'image', 'video'
    file = models.FileField(upload_to='media/', null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return self.title
    

