from django import forms
from models import Vote


VOTE_CHOICES = ((0, 'Skip'),
                (-1, 'No'),
                (1, 'Probably'),
                (2, 'Definetely'))


class VoteForm(forms.ModelForm):
    """Voting Form."""
    class Meta:
        model = Vote
        fields = ('vote',)
