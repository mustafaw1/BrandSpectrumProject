from django.shortcuts import render
from rest_framework import generics
from .models import Campaign
from .serializers import CampaignSerializer
from .serializers import CampaignCreateSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()
from .permission import IsBrandManagerPermission
from django.db.models import Q



# class CampaignListView(generics.ListCreateAPIView):
#     queryset = Campaign.objects.all()
#     serializer_class = CampaignSerializer


class CampaignCreateView(generics.CreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


from django.db.models import Q

class CampaignListView(generics.ListAPIView):
    serializer_class = CampaignSerializer

    def get_queryset(self):
        user = self.request.user  # Get the logged-in user.

        if user.is_authenticated:
            # Filter campaigns based on user type
            if user.is_influencer:
                # Influencer: Campaigns the user is associated with
                queryset = Campaign.objects.filter(influencers=user)

            elif user.is_brand_manager:
                # Brand Manager: Campaigns created by the user
                queryset = Campaign.objects.filter(brand_manager=user)

            else:
                # Other user types: No specific filtering
                queryset = Campaign.objects.all()
        else:
            # Not authenticated: Only public campaigns
            queryset = Campaign.objects.filter(is_public=True)

        return queryset
