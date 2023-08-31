"""
URL configuration for brandspectrum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from influencers.views import UserListCreateView
from accounts.views import CustomUserListCreateView, CustomUserDetailView
from campaigns.views import CampaignListView, CampaignDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register-influencer/', UserListCreateView.as_view(), name='influencer-registration'),
    path('api/users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('api/campaigns/', CampaignListView.as_view(), name='campaign-list'),
    path('api/campaigns/<int:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),
]


