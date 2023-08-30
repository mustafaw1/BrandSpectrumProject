from django.urls import path
from .views import InfluencerListCreateView

urlpatterns = [
    path('influencers/', InfluencerListCreateView.as_view(), name='influencer-list-create'),
]
