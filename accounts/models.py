from django.db import models
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .choices import USER_TYPE_CHOICES 
from brandmanagers.models import BrandManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)
    
class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    is_brand_manager = models.BooleanField(default=False)
    is_influencer = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    influencer_profile = models.OneToOneField('influencers.InfluencerRegistration', on_delete=models.CASCADE, related_name='user_influencer_profile', null=True)
    is_influencer_registered = models.BooleanField(default=False)

    brand_manager_profile = models.OneToOneField('brandmanagers.BrandManager', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


