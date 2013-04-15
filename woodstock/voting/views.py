from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from models import MozillianProfile, Vote

import forms
import json
import os

PROJECT_DIR = os.path.dirname(__file__)
countries_codes = open(os.path.join(PROJECT_DIR, 'countries.json')).read()
COUNTRIES = json.loads(countries_codes)
VOTE_CHOICES = {0: 'Skip',
                -1: 'No',
                1: 'Probably',
                2: 'Definitely'}


def login_required_view(request):
    messages.info(request, 'You must login first')
    return redirect('main')


def main(request):
    """Main page view."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    else:
        return render(request, 'index.html')


@login_required
def dashboard(request):
    user = request.user
    mozillians = MozillianProfile.objects.all()
    mozillians_count = mozillians.count()
    votes_count = Vote.objects.all().count()

    if mozillians_count == 0:
        status = 0
    else:
        status = int(round(100*float(votes_count)/float(mozillians_count)))

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
    else:
        instance = Vote(voter=request.user, nominee=mozillian)
    vote_form = forms.VoteForm(data=request.POST or None,
                               instance=instance)
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
