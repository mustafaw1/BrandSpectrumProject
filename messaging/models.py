from django.db import models
from accounts.models import CustomUser


class Conversation(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        CustomUser, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.sender} and {self.receiver}"
