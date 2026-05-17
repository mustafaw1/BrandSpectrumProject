from .models import Conversation


def process_websocket_message(sender, recipient, message_content):
    conversation = Conversation(
        sender=sender, receiver=recipient, content=message_content
    )
    conversation.save()
