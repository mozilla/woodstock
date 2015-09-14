from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse

from django_browserid.http import JSONResponse
from django_browserid.views import Verify

from models import Application, MozillianProfile, Vote, Event

import forms


class BrowserIDVerify(Verify):

    def login_failure(self, msg=''):
        if not msg:
            msg = (u'Login failed. Please make sure that you have a verified '
                   u'email and an account register to this site.')
        messages.warning(self.request, msg)
        return JSONResponse({'redirect': self.failure_url})


def main(request):
    """Main page view."""
    if request.user.is_authenticated():
        return redirect(reverse('voting_events'))
    return render(request, 'index.html')


def _get_percentage(partial, total):
    """Get the percentage."""
    return int(round(100*float(partial)/float(total)))


@login_required
def events(request):
    user = request.user
    events = Event.objects.all()

    return render(request, 'events.html',
                  {'user': user, 'events': events})


@login_required
def dashboard(request):
    # Parse blind/event values
    blind = bool(int(request.GET.get('blind', u'1')))
    event_param = request.GET.get('events', u'1,2,3')
    event_ids = map(lambda x: int(x), event_param.split(','))

    user = request.user
    applications = Application.objects.filter(event__id__in=event_ids)
    mozillians = MozillianProfile.objects.filter(application__in=applications)
    mozillians_count = mozillians.count()
    status = {}
    votes = Vote.objects.filter(voter=user, nominee__in=mozillians)
    votes_count = votes.count()

    if mozillians_count == 0:
        status['total'] = 0
        status['no'] = 0
        status['definetely'] = 0
        status['skip'] = 0
        status['positive'] = 0
    else:
        status['total'] = _get_percentage(votes_count, mozillians_count)
        status['no'] = _get_percentage(votes.filter(vote=-1).count(),
                                       mozillians_count)
        status['definitely'] = _get_percentage(votes.filter(vote=2).count(),
                                               mozillians_count)
        status['skip'] = _get_percentage(votes.filter(vote=0).count(),
                                         mozillians_count)
        status['positive'] = _get_percentage(votes.filter(vote=1).count(),
                                             mozillians_count)

    ctx = {
        'user': user,
        'status': status,
        'mozillians': mozillians,
        'blind': blind,
        'event_ids': event_ids
    }
    return render(request, 'dashboard.html', ctx)


@login_required
def view_voting(request, slug):
    """View voting and cast a vote view."""

    # Parse blind/event values
    blind = bool(int(request.GET.get('blind', u'1')))
    event_param = request.GET.get('events', u'1,2,3')
    event_ids = map(lambda x: int(x), event_param.split(','))
    applications = Application.objects.filter(event__id__in=event_ids)
    mozillian_qs = MozillianProfile.objects.filter(application__in=applications)

    mozillian = get_object_or_404(MozillianProfile, slug=slug)
    if mozillian.votes.filter(voter=request.user).exists():
        instance = mozillian.votes.get(voter=request.user)
        extra = instance.vote
    else:
        instance = Vote(voter=request.user, nominee=mozillian)
        extra = None
    vote_form = forms.VoteForm(data=request.POST or None,
                               instance=instance,
                               initial={'vote': extra})
    # Check POST data and save form
    next_entry = mozillian.get_next_entry(mozillian_qs) or None
    previous_entry = mozillian.get_previous_entry(mozillian_qs) or None

    if vote_form.is_valid():
        vote_form.save()
        if next_entry:
            return redirect('voting_view_voting', slug=next_entry.slug)
        return redirect(dashboard)

    ctx = {
        'mozillian': mozillian,
        'vote_form': vote_form,
        'next_entry': next_entry,
        'previous_entry': previous_entry,
        'blind': blind,
        'event_ids': event_ids
    }
    return render(request, 'vote.html', ctx)
