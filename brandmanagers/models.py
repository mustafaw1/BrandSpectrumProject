from django.db import models
from django.db import models
from accounts.choices import USER_TYPE_CHOICES


class BrandManager(models.Model):
    name = models.CharField(max_length=225)
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='brand_manager')
    
    def __str__(self):
        return self.name



