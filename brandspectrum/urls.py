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
from influencers.views import Influencer_Registration
from accounts.views import CustomUserListCreateView, CustomUserDetailView
from campaigns.views import CampaignListView
from campaigns.views import CampaignCreateView
from influencers.views import influencer_dashboard
from influencers.views import influencer_signup
from influencers.views import InfluencerLoginView
from brandmanagers.views import brand_manager_dashboard
from django.contrib.auth import views as auth_views
from brandmanagers.views import brand_manager_signup, BrandManagerLoginView, content_approval, content_submission


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/influencer_signup/',influencer_signup, name='signup'),
    path('api/influencer_login/', InfluencerLoginView.as_view(template_name='registration/influencer_login.html'), name='login'),
    path('api/influencer_registration/', Influencer_Registration.as_view(), name='influencer_registration'),
    path('api/users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('api/campaigns/create/', CampaignCreateView.as_view(), name='campaign-create'),
    path('api/campaigns/', CampaignListView.as_view(), name='campaign-list'),
    path('api/influencer_dashboard/', influencer_dashboard, name='influencer-dashboard'),
    path('api/logout_influencer/', auth_views.LogoutView.as_view(), name='logout_influencer'),
    path('api/brandmanager_signup/', brand_manager_signup, name='brand_manager_signup'),
    path('api/brandmanager_login/', BrandManagerLoginView.as_view(template_name='registration/brandmanager_login.html'), name='brand_manager_login'),
    path('api/logout_brandmanager/', auth_views.LogoutView.as_view(), name='logout_brandmanager'),
    path('api/brandmanager_dashboard/', brand_manager_dashboard, name='brandmanager_dashboard'),
    path('api/influencer_contentsubmission/', content_submission, name='content_submission'),
    path('api/content_approval/', content_approval, name='content_approval'),
]


