from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import InfluencerRegistration
from .serializers import InfluencerSerializer
from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer
from rest_framework.permissions import IsAuthenticated


class UserListCreateView(generics.ListCreateAPIView):
    queryset = InfluencerRegistration.objects.all()
    serializer_class = InfluencerSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfluencerRegistration.objects.all()
    serializer_class = InfluencerSerializer


class InfluencerDashboardView(APIView):

    def get(self, request):
        user = request.user
        campaigns = Campaign.objects.filter(brand_manager=user)
        campaign_serializer = CampaignSerializer(campaigns, many=True)

        return Response({
            'campaigns': campaign_serializer.data,
        })
