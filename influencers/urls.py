from django.urls import path
from .views import UserListCreateView

urlpatterns = [
    path('influencers/', UserListCreateView.as_view(), name='influencer-list-create'),
]
