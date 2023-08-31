from rest_framework import serializers
from .models import InfluencerRegistration
from accounts.models import CustomUser

class InfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerRegistration
        fields = '__all__'