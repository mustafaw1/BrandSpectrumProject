from mailbox import Message
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Conversation
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import CustomUser


@login_required
def brand_manager_messaging(request, username):
    user = request.user  # Get the currently logged in brand manager

    if user.is_brand_manager:
        # Brand managers should be able to view messages here
        recipient = get_object_or_404(get_user_model(), username=username)

        if request.method == "POST":
            message_content = request.POST.get("message")

            conversation = Conversation(
                sender=user, receiver=recipient, content=message_content
            )
            conversation.save()

        # Retrieve the conversation messages between the brand manager and the recipient
        conversations = Conversation.objects.filter(
            (Q(sender=user, receiver=recipient) | Q(sender=recipient, receiver=user))
        ).order_by("timestamp")

        return render(
            request,
            "registration/brand_manager_messaging.html",
            {
                "conversations": conversations,
                "recipient": recipient,
            },
        )
    else:
        return HttpResponse("Unauthorized access")


@login_required
def influencer_messaging(request, username):
    user = request.user

    if user.is_influencer:
        recipient = get_object_or_404(get_user_model(), username=username)

        if request.method == "POST":
            message_content = request.POST.get("message")

            conversation = Conversation(
                sender=user, receiver=recipient, content=message_content
            )
            conversation.save()

        # Retrieve the conversation messages between the brand manager and the recipient
        conversations = Conversation.objects.filter(
            (Q(sender=user, receiver=recipient) | Q(sender=recipient, receiver=user))
        ).order_by("timestamp")

        return render(
            request,
            "registration/influencers_messaging.html",
            {
                "conversations": conversations,
                "recipient": recipient,
            },
        )
    else:
        return HttpResponse("Unauthorized access")
