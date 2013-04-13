from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from models import MozillianProfile, Vote


VOTE_CHOICES = ((0, 'Skip'),
                (-1, 'No'),
                (1, 'Probably'),
                (2, 'Definetely'))


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """Render RadioSelect Horizontally."""
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class HorizontalRadioSelect(forms.widgets.RadioSelect):
    """Horizontal Radioselect."""
    renderer = HorizontalRadioRenderer


class VoteForm(forms.Form):
    """Voting Form."""
    def __init__(self, nominee, voter, *args, **kwargs):
        """Initialize form.
        Dynamically set fields.
        """
        super(VoteForm, self).__init__(*args, **kwargs)
        initial_data = 0
        if Vote.objects.filter(voter=voter, nominee=nominee).exists():
            initial_data = (Vote.objects
                            .filter(voter=voter, nominee=nominee)[0].vote)
        self.fields['mozillian_vote__%s__%s'
                    % (str(nominee.id), str(voter.id))] = (
                        forms.ChoiceField(
                            widget=HorizontalRadioSelect(),
                            initial=initial_data,
                            choices=VOTE_CHOICES,
                            label=''))

    def save(self, *args, **kwargs):
        cdata = self.cleaned_data
        for field, votes in cdata.items():
            nominee_id = field.split('__')[1]
            voter_id = field.split('__')[2]
            voter = get_object_or_404(User, pk=voter_id)
            nominee = get_object_or_404(MozillianProfile, pk=nominee_id)
            vote_obj = get_object_or_404(Vote, voter=voter, nominee=nominee)
            vote_obj.vote = int(votes)
            vote_obj.save()
