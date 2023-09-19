from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from campaigns.models import Campaign, InfluencerContentApproval
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from accounts.forms import BrandManagerSignupForm
from django.shortcuts import render, get_object_or_404, redirect
from campaigns.models import Campaign, InfluencerContentApproval, InfluencerContentSubmission
from django.contrib.auth.views import LoginView 
from brandspectrum import settings
from django.core.mail import send_mail
from campaigns.forms import ContentApprovalForm
from campaigns.forms import ContentSubmissionForm, RejectionForm
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
            return redirect('brandmanager_dashboard')
        messages.error(self.request, 'Invalid credentials.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials.')
        print('invalid')
        return super().form_invalid(form)




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
            
            submission.influencer = request.user

            brand_manager_email = form.cleaned_data.get('brand_manager_email')

            submission.save()

            # Notify the influencer
            influencer_email = request.user.email
            influencer_subject = 'Content Submission Confirmation'
            influencer_message = 'Your content submission has been received and is awaiting approval.'
            send_mail(influencer_subject, influencer_message, settings.EMAIL_HOST_USER, [influencer_email], fail_silently=True)

            # Notify the brand manager (use the provided email)
            brand_manager_subject = 'New Content Submission Request'
            brand_manager_message = f'Influencer {request.user.username} has submitted new content for approval. Check the dashboard for details.'
            send_mail(brand_manager_subject, brand_manager_message, settings.EMAIL_HOST_USER, [brand_manager_email], fail_silently=True)

            messages.success(request, 'Content submitted successfully. Awaiting approval.')
            return HttpResponse('Content submitted successfully. Awaiting approval.')
    else:
        form = ContentSubmissionForm()

    context = {'form': form}
    return render(request, 'registration/influencer_contentsubmission.html', context)




@login_required(login_url=settings.BRAND_MANAGER_LOGIN_URL)
def content_approval(request):
    pending_submissions = InfluencerContentSubmission.objects.filter(is_approved=False)
    rejection_form = RejectionForm()

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        action = request.POST.get('action')

        submission = get_object_or_404(InfluencerContentSubmission.objects.all(), pk=submission_id)

        if action == 'approve':
            submission.is_approved = True
            submission.save()

            influencer_email = submission.influencer.email
            influencer_subject = 'Content Approved'
            influencer_message = 'Your content submission has been approved.'
            send_mail(influencer_subject, influencer_message, settings.EMAIL_HOST_USER, [influencer_email], fail_silently=True)

            messages.success(request, 'Content approved successfully.')

        elif action == 'reject':
            rejection_form = RejectionForm(request.POST)

            if rejection_form.is_valid():
                submission.is_approved = False
                submission.save()

                influencer_email = submission.influencer.email
                influencer_subject = 'Content Rejected'
                influencer_message = f'Your content submission has been rejected. Reason: {rejection_form.cleaned_data["rejection_reason"]}'
                send_mail(influencer_subject, influencer_message, settings.EMAIL_HOST_USER, [influencer_email], fail_silently=True)
                messages.success(request, 'Content rejected successfully.')
            else:
                messages.error(request, 'Invalid rejection form. Please provide a reason.')

    context = {'pending_submissions': pending_submissions, 'rejection_form': rejection_form}
    return render(request, 'registration/influencer_content_approval.html', context)
