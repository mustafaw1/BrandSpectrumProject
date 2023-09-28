from django.shortcuts import render
from campaigns.models import Campaign
from influencers.models import InfluencerRegistration
from brandmanagers.models import BrandManager
from brandmanagers.forms import BrandManagerForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import SuperAdminSignupForm
from django.contrib.auth import login
from brandspectrum import settings
from django.views import View
from django.contrib.auth.decorators import login_required


class SuperAdminSignupView(View):
    template_name = 'registration/superadmin_signup.html'  
    
    def get(self, request):
        form = SuperAdminSignupForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = SuperAdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_super_admin = True 
            user.save()
            login(request, user)
            return redirect('superadmin_dashboard')  
        return render(request, self.template_name, {'form': form})

    


# @login_required(login_url=settings.SUPERADMIN_LOGIN_URL)
def superadmin_dashboard(request):
    # Existing code to fetch data for active campaigns, completed campaigns,
    # registered influencers, and non-registered influencers.
    active_campaigns = Campaign.objects.filter(status='Active')
    completed_campaigns = Campaign.objects.filter(status='Completed')
    registered_influencers = InfluencerRegistration.objects.filter(isRegistered=True)
    non_registered_influencers = InfluencerRegistration.objects.filter(isRegistered=False)
    brand_managers = BrandManager.objects.all()

    # Filtering influencers based on search parameters.
    name = request.GET.get('name')
    age = request.GET.get('age')
    children = request.GET.get('children')
    category = request.GET.get('category')
    gender = request.GET.get('gender')

    influencers = InfluencerRegistration.objects.all()

    if name:
        influencers = influencers.filter(name__icontains=name)
    if age:
        influencers = influencers.filter(age=age)
    if children:
        influencers = influencers.filter(children=children)
    if gender:
        influencers = influencers.filter(gender=gender)
    if category:
        influencers = influencers.filter(category=category)

    # Existing context data.
    context = {
        'active_campaigns': active_campaigns,
        'completed_campaigns': completed_campaigns,
        'registered_influencers': registered_influencers,
        'non_registered_influencers': non_registered_influencers,
        'brand_managers': brand_managers,
        'influencers': influencers
    }

    # Handling adding or deleting Brand Managers/Clients.
    if request.method == 'POST':
        response = manage_brand_managers(request)
        if response:
            return response  

    return render(request, 'registration/superadmin_dashboard.html', context)

# Function to manage Brand Managers/Clients.
def manage_brand_managers(request, pk=None):
    brand_managers = BrandManager.objects.all()
    form = BrandManagerForm()

    if request.method == 'POST':
        if pk:
            brand_manager = get_object_or_404(BrandManager, pk=pk)
            form = BrandManagerForm(request.POST, instance=brand_manager)
        else:
            form = BrandManagerForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Brand Manager/Client saved successfully.')
            return redirect('superadmin_dashboard')

    # Handle deleting Brand Managers/Clients
    if request.method == 'POST' and 'delete' in request.POST:
        brand_manager_id = request.POST.get('brand_manager_id')
        brand_manager = get_object_or_404(BrandManager, pk=brand_manager_id)
        brand_manager.delete()
        messages.success(request, 'Brand Manager/Client deleted successfully.')
        return redirect('superadmin_dashboard')

    return render(request, 'registration/superadmin_dashboard.html', {'brand_managers': brand_managers, 'form': form})




@login_required(login_url=settings.SUPERADMIN_LOGIN_URL)
def manage_brand_managers(request, pk=None):
    brand_managers = BrandManager.objects.all()
    if request.method == 'POST':
        if pk:
            brand_manager = get_object_or_404(BrandManager, pk=pk)
            form = BrandManagerForm(request.POST, instance=brand_manager)
        else:
            form = BrandManagerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand Manager/Client saved successfully.')
            return HttpResponse('Brand Manager/Client saved successfully.')
    else:
        if pk:
            brand_manager = get_object_or_404(BrandManager, pk=pk)
            form = BrandManagerForm(instance=brand_manager)
        else:
            form = BrandManagerForm()

    # Handle deleting Brand Managers/Clients
    if request.method == 'POST' and 'delete' in request.POST:
        brand_manager_id = request.POST.get('brand_manager_id')
        brand_manager = get_object_or_404(BrandManager, pk=brand_manager_id)
        brand_manager.delete()
        messages.success(request, 'Brand Manager/Client deleted successfully.')
        return HttpResponse('Brand Manager/Client deleted successfully.')

    return render(request, 'registration/manage_brand_managers.html', {'brand_managers': brand_managers, 'form': form})




