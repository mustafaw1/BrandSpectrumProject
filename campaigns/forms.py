from django import forms
from .models import InfluencerContentSubmission

class ContentApprovalForm(forms.Form):
    content_id = forms.IntegerField(widget=forms.HiddenInput())
    approval_status = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.RadioSelect(),
        required=True,
    )

class ContentSubmissionForm(forms.ModelForm):
    class Meta:
        model = InfluencerContentSubmission
        fields = ['content_type', 'content_text', 'content_image', 'content_video']

    def __init__(self, *args, **kwargs):
        super(ContentSubmissionForm, self).__init__(*args, **kwargs)