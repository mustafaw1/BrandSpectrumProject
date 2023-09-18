from rest_framework import generics
from .models import InfluencerRegistration
from .serializers import InfluencerSerializer
from django.contrib.auth import login
from accounts.forms import InfluencerSignupForm
from django.shortcuts import render, redirect
from accounts.forms import InfluencerSignupForm  
from django.contrib.auth.views import LoginView 
from django.contrib import messages
from django.http import HttpResponseBadRequest
from influencers.models import InfluencerRegistration
from django.contrib.auth.decorators import login_required
from campaigns.models import Campaign
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from brandspectrum import settings

def influencer_signup(request):
    if request.method == 'POST':
        form = InfluencerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_influencer = True  
            user.save()  
            login(request, user)
            messages.success(request, 'You have successfully registered as an influencer.')
            return redirect('login')  
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'Error in {field}: {error}')
            
            response_content = '<br>'.join(error_messages)
            return HttpResponseBadRequest(response_content)
    else:
        form = InfluencerSignupForm()
    return render(request, 'registration/signup_influencer.html', {'form': form})



class InfluencerLoginView(LoginView):
    def form_valid(self, form):
        if self.request.user.is_authenticated and self.request.user.is_influencer:
            print("Redirecting to influencer_registration")
            return redirect('influencer_registration')
        else:
            print("User is not an influencer")
            messages.info(self.request, 'You are not an influencer.')
            return redirect('signup')
        return super().form_valid(form) 

    

class Influencer_Registration(generics.CreateAPIView):
    serializer_class = InfluencerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming you have a way to determine if registration is complete, e.g., a flag in the request data
        is_registration_complete = serializer.validated_data.get('is_registration_complete', False)

        # Create the influencer record
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

    
        if is_registration_complete:
            influencer = InfluencerRegistration.objects.get(user=request.user)
            influencer.isRegistered = True
            influencer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfluencerRegistration.objects.all()
    serializer_class = InfluencerSerializer


@login_required(login_url=settings.LOGIN_URL) 
def influencer_dashboard(request):
    try:
        user = request.user
        print(user)
        if request.user.is_influencer and request.user.is_influencer_registered :
            influencer_registration = user.influencer_registration_user
            campaigns = Campaign.objects.filter(influencers_registration=request.user.influencer_registration_user)
            data = {'influencer': influencer_registration, 'campaigns': campaigns}
            return render(request, 'registration/influencer_dashboard.html', data)
        else:
            messages.error(request, 'You are not an influencer or not registered as an influencer.')
            return redirect('login')
    except get_user_model().DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')



