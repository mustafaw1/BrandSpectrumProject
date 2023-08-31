from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import InfluencerRegistration
from .serializers import InfluencerSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = InfluencerRegistration.objects.all()
    serializer_class = InfluencerSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfluencerRegistration.objects.all()
    serializer_class = InfluencerSerializer

