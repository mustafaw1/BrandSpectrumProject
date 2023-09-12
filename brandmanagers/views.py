from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from campaigns.models import Campaign, InfluencerContentApproval
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from accounts.forms import BrandManagerSignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView 
from brandspectrum import settings



def brand_manager_signup(request):
    if request.method == 'POST':
        form = BrandManagerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_brand_manager = True
            user.save()
            login(request, user)
            return redirect('brand_manager_login')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'Error in {field}: {error}')

            response_content = '<br>'.join(error_messages)
            return HttpResponseBadRequest(response_content)
    else:
        form = BrandManagerSignupForm()
    return render(request, 'registration/brandmanager_signup.html', {'form': form})


class BrandManagerLoginView(LoginView):
    template_name = 'registration/brandmanager_login.html'
    def form_valid(self, form):
        if self.request.user.is_authenticated and self.request.user.is_brand_manager:
            print('Redirecting to the brand manager dashboard')
            return redirect('brandmanager_dashboard')
        else:
            print('User is not authenticated or not a brand manager')
            messages.info(self.request, 'You are not a brand manager.')
            return redirect('brand_manager_signup')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials for brand manager.')
        return HttpResponseBadRequest('Invalid login credentials for brand manager.')



@login_required(login_url=settings.BRAND_MANAGER_LOGIN_URL)
def brand_manager_dashboard(request):
    brand_manager = request.user.is_brand_manager
    print(brand_manager)
    if not request.user.is_brand_manager:
        return HttpResponseForbidden("Access Denied")

    brand_manager = request.user
    all_campaigns = Campaign.objects.all()

    active_campaigns = Campaign.objects.filter(status='Active', brand_manager=brand_manager)
    completed_campaigns = Campaign.objects.filter(status='Completed', brand_manager=brand_manager)
    inactive_campaigns = Campaign.objects.filter(status='Inactive', brand_manager=brand_manager)

    
    influencer_name = request.GET.get('influencer_name', '')  

    if influencer_name:
        active_campaigns = active_campaigns.filter(influencers_registration__name__icontains=influencer_name)
        completed_campaigns = completed_campaigns.filter(influencers_registration__name__icontains=influencer_name)
        inactive_campaigns = inactive_campaigns.filter(influencers_registration__name__icontains=influencer_name)

    context = {
        'all_campaigns': all_campaigns,
        'active_campaigns': active_campaigns,
        'completed_campaigns': completed_campaigns,
        'inactive_campaigns': inactive_campaigns,
        'influencer_name': influencer_name,
    }

    return render(request, 'registration/brandmanager_dashboard.html', context)


