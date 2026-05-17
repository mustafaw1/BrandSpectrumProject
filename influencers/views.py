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
from django.http import HttpResponse
from messaging.models import Conversation
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from accounts.models import CustomUser


def influencer_signup(request):
    if request.method == "POST":
        form = InfluencerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_influencer = True
            user.save()
            login(request, user)
            messages.success(
                request, "You have successfully registered as an influencer."
            )
            return redirect("influencer_login")
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"Error in {field}: {error}")

            response_content = "<br>".join(error_messages)
            return HttpResponseBadRequest(response_content)
    else:
        form = InfluencerSignupForm()
    return render(request, "registration/signup_influencer.html", {"form": form})


class InfluencerLoginView(LoginView):
    def form_valid(self, form):
        if self.request.user.is_authenticated and self.request.user.is_influencer:
            return redirect("influencer-dashboard")
        messages.error(self.request, "Invalid credentials.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Display an error message for invalid credentials
        messages.error(self.request, "Invalid credentials.")
        return super().form_invalid(form)


class Influencer_Registration(generics.CreateAPIView):
    serializer_class = InfluencerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming you have a way to determine if registration is complete, e.g., a flag in the request data
        is_registration_complete = serializer.validated_data.get(
            "is_registration_complete", False
        )

        # Create the influencer record
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        if is_registration_complete:
            influencer = InfluencerRegistration.objects.get(user=request.user)
            influencer.isRegistered = True
            influencer.save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfluencerRegistration.objects.all()
    serializer_class = InfluencerSerializer


@login_required(login_url=settings.Influencer_LOGIN_URL)
def influencer_dashboard(request):
    try:
        user = request.user
        if user.is_influencer and user.is_influencer_registered:
            influencer_registration = InfluencerRegistration.objects.get(user=user)
            influencer_name = influencer_registration.name
            influencer_age = influencer_registration.age
            campaigns = Campaign.objects.filter(
                influencers_registration=influencer_registration
            )

            if request.method == "POST":
                recipient_username = request.POST.get("recipient_username")
                message_content = request.POST.get("message_content")
                recipient = get_object_or_404(
                    get_user_model(), username=recipient_username
                )

                message = Conversation(
                    sender=user, receiver=recipient, content=message_content
                )
                message.save()
            user = request.user

            # Fetch the list of brand managers who have messaged the influencer
            brand_managers = CustomUser.objects.filter(
                sent_messages__receiver=user, is_brand_manager=True
            )

            # Retrieve the influencer's messages
            messages = Conversation.objects.filter(
                Q(sender=user, receiver__in=brand_managers)
                | Q(sender__in=brand_managers, receiver=user)
            ).order_by("-timestamp")
            data = {
                "influencer_registration": influencer_registration,
                "campaigns": campaigns,
                "influencer_name": influencer_name,
                "influencer_age": influencer_age,
                "messages": messages,
            }

            return render(request, "registration/influencer_dashboard.html", data)
        else:
            messages.error(
                request, "You are not an influencer or not registered as an influencer."
            )
            return redirect("influlogin")
    except InfluencerRegistration.DoesNotExist:
        messages.error(request, "Influencer registration not found for this user.")
        return redirect("influecner_login")
