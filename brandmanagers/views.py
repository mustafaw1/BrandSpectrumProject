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
from django.core.mail import send_mail
from campaigns.forms import ContentApprovalForm
from campaigns.forms import ContentSubmissionForm
from django.http import HttpResponse
from influencers.models import InfluencerRegistration
from brandmanagers.models import BrandManager

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



@login_required(login_url=settings.LOGIN_URL) 
def content_submission(request):
    if request.method == 'POST':
        form = ContentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            influencer_user = request.user
            submission.influencer = influencer_user
            submission.save()
            influencer_email = request.user.email
            print(influencer_email)
            influencer_subject = 'Content Submission Confirmation'
            influencer_message = 'Your content submission has been received and is awaiting approval.'
            send_mail(influencer_subject, influencer_message, settings.EMAIL_HOST_USER, [influencer_email], fail_silently=True)
            # Notify the selected brand manager (retrieve brand manager's email from the influencer_registration)
            try:
                brand_manager_email = Campaign.brand_manager.name
                print(brand_manager_email)
                brand_manager_subject = 'New Content Submission Request'
                brand_manager_message = f'Influencer {request.user.username} has submitted new content for approval. Check the dashboard for details.'
                send_mail(brand_manager_subject, brand_manager_message, settings.EMAIL_HOST_USER, [brand_manager_email], fail_silently=True)

                messages.success(request, 'Content submitted successfully. Awaiting approval.')
            except AttributeError:
                messages.error(request, 'Error: Brand manager email not found.')

            return HttpResponse('Brand manager email is not found')
    else:
        form = ContentSubmissionForm()

    context = {'form': form}
    return render(request, 'registration/influencer_contentsubmission.html', context)


           
    


@login_required(login_url=settings.BRAND_MANAGER_LOGIN_URL)
def content_approval(request):
    if not request.user.is_brand_manager:
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        form = ContentApprovalForm(request.POST)
        if form.is_valid():
            # Process the form data and approve/reject the content
            is_approved = form.cleaned_data['approval_status'] == 'approve'
            content_id = form.cleaned_data['content_id']
            
            content = get_object_or_404(InfluencerContentApproval, pk=content_id)
            content.is_approved = is_approved
            content.save()
            return redirect('brandmanager_dashboard')
    else:
        # Handle GET request here if needed
        form = ContentApprovalForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/influencer_content_approval.html', context)

