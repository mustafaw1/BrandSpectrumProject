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
    brand_manager_email = forms.EmailField(label='Brand Manager Email', required=True)

    class Meta:
        model = InfluencerContentSubmission
        fields = ['content_type', 'content_text', 'content_image', 'content_video', 'brand_manager_email']


class RejectionForm(forms.Form):
    rejection_reason = forms.CharField(widget=forms.Textarea)