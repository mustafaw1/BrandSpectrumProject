from django.utils import timezone
from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from accounts.choices import USER_TYPE_CHOICES


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='campaign_images/')
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='Influencer')
    is_public = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    influencers = models.ManyToManyField(get_user_model(), related_name='campaigns', blank=True)
    media_type = models.CharField(max_length=20, default=None)  # e.g., 'image', 'video'
    file = models.FileField(upload_to='media/', null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    feedback = models.TextField(blank=True)

    brand_manager = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='campaigns_managed',
        null=True,
        blank=True,
    )


    def __str__(self):
        return self.title


class InfluencerContentApproval(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    influencer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Content from {self.influencer} for {self.campaign} - Approved: {self.is_approved}"
    

class InfluencerContentSubmission(models.Model):
    influencer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ])
    content_text = models.TextField(blank=True, null=True)  # For text content
    content_image = models.ImageField(upload_to='content_images/', blank=True, null=True)  # For images
    content_video = models.FileField(upload_to='content_videos/', blank=True, null=True)  # For videos
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Content from {self.influencer} - Type: {self.content_type} - Approved: {self.is_approved}"




