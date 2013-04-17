from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from models import MozillianProfile, Vote

import forms


def login_required_view(request):
    messages.info(request, 'Please login first.')
    return redirect('main')


def main(request):
    """Main page view."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    return render(request, 'index.html')


def _get_percentage(partial, total):
    """Get the percentage."""
    return int(round(100*float(partial)/float(total)))


@login_required
def dashboard(request):
    user = request.user
    mozillians = MozillianProfile.objects.all()
    mozillians_count = mozillians.count()
    status = {}
    votes = Vote.objects.filter(voter=user)
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

    return render(request, 'dashboard.html',
                  {'user': user,
                   'status': status,
                   'mozillians': mozillians})


def login_failed(request):
    """Redirect to login page on login failure."""
    messages.warning(request, ('Login failed. Please make sure that you '
                               'have an account, and your email '
                               'is verified.'))
    return render(request, 'index.html')


@login_required
def view_voting(request, slug):
    """View voting and cast a vote view."""
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
    if vote_form.is_valid():
        vote_form.save()
        next_entry = mozillian.get_next_entry()
        if next_entry:
            return redirect('voting_view_voting', slug=next_entry.slug)
        return redirect(dashboard)

    return render(request, 'vote.html',
                  {'mozillian': mozillian,
                   'vote_form': vote_form})
