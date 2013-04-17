from django import forms
from models import Vote


class VoteForm(forms.ModelForm):
    """Voting Form."""
    class Meta:
        model = Vote
        fields = ['vote']
        widgets = {'vote': forms.RadioSelect()}
