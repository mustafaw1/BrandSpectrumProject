from django import forms


class ComposeMessageForm(forms.Form):
    receiver = forms.CharField(max_length=255, label="Recipient")
    content = forms.CharField(widget=forms.Textarea, label="Message Content")


class MessageHistoryForm(forms.Form):
    user_id = forms.IntegerField(label="User ID")
