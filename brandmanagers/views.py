from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from campaigns.models import Campaign, InfluencerContentApproval
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from accounts.forms import BrandManagerSignupForm
from django.shortcuts import render, get_object_or_404, redirect
from campaigns.models import Campaign, InfluencerContentApproval
from django.contrib.auth.views import LoginView 
from brandspectrum import settings

def brand_manager_signup(request):
    if request.method == 'POST':
        form = BrandManagerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_brand_manager = True
            user.user_type = form.cleaned_data['user_type'] 
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
    def form_valid(self, form):
        if self.request.user.is_authenticated and self.request.user.is_brand_manager:
            messages.success(self.request, 'You are logged in as a brand manager.')
            return redirect('brandmanager_dashboard')
        else:
            print('invalid')
            messages.error(self.request, 'Invalid login credentials for brand manager.')
            return redirect('brand_manager_signup')
        return super().form_valid(form) 




@login_required(login_url=settings.BRAND_MANAGER_LOGIN_URL)
def brand_manager_dashboard(request):
    if not request.user.is_brand_manager:
        return HttpResponseForbidden("Access Denied")
    

    influencer_name = request.GET.get('influencer_name', '')

    active_campaigns = Campaign.objects.filter(
        status='Active',
        influencers_registration__name__icontains=influencer_name,
    )
    completed_campaigns = Campaign.objects.filter(
        status='Completed',
        influencers_registration__name__icontains=influencer_name,
    )
    inactive_campaigns = Campaign.objects.filter(
        status='Inactive',
        influencers_registration__name__icontains=influencer_name,
    )

    pending_content = InfluencerContentApproval.objects.filter(
        is_approved=False,
        campaign__brand_manager=request.user,
    )


    all_campaigns = Campaign.objects.all()

    context = {
        'all_campaigns': all_campaigns,
        'active_campaigns': active_campaigns,
        'completed_campaigns': completed_campaigns,
        'inactive_campaigns': inactive_campaigns,
        'influencer_name': influencer_name,
    }

    return render(request, 'registration/brandmanager_dashboard.html', context)


def content_approval(request, content_id):
    # Ensure that the user is a brand manager
    if not request.user.is_brand_manager:
        return HttpResponseForbidden("Access Denied")

    content = get_object_or_404(InfluencerContentApproval, pk=content_id)

    # Handle content approval
    if request.method == 'POST':
        is_approved = request.POST.get('approval_status') == 'approve'
        content.is_approved = is_approved
        content.save()

        # Redirect back to the content approval dashboard
        return redirect('brandmanager_dashboard')

    context = {
        'content': content,
    }

    return render(request, 'content_approval.html', context)

