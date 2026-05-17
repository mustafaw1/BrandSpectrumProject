from django.shortcuts import render
from rest_framework import generics
from .models import Campaign
from .serializers import CampaignSerializer
from .serializers import CampaignCreateSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()




# class CampaignListView(generics.ListCreateAPIView):
#     queryset = Campaign.objects.all()
#     serializer_class = CampaignSerializer


class CampaignCreateView(generics.CreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer




class CampaignListView(generics.ListAPIView):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()

  