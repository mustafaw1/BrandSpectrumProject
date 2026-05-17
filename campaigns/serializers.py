from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    # Include fields from related objects
    brand_manager_username = serializers.ReadOnlyField(source='brand_manager.username')
    brand_manager_email = serializers.ReadOnlyField(source='brand_manager.email')

    class Meta:
        model = Campaign
        fields = '__all__'
class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'start_date', 'end_date', 'image', 'is_public']

