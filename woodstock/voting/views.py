from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from models import MozillianProfile, Vote

import forms
import json
import os


countries_codes = (open(os.path.join(settings.MEDIA_ROOT, 'js/countries.json'))
                   .read())
COUNTRIES = json.loads(countries_codes)
VOTE_CHOICES = {0: 'Skip',
                -1: 'No',
                1: 'Probably',
                2: 'Definitely'}


def main(request):
    """Main page view."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    else:
        return render(request, 'index.html')


def dashboard(request):
    user = request.user
    if user.is_authenticated():
        mozillians_data = {}
        mozillians = MozillianProfile.objects.all()
        mozillians_count = mozillians.count()

        for mozillian in mozillians:
            vote = Vote.objects.filter(voter=user, nominee=mozillian)
            if vote:
                mozillians_data[mozillian] = VOTE_CHOICES[vote[0].vote]
            else:
                mozillians_data[mozillian] = None

        votes = Vote.objects.filter(voter=user).count()

        if mozillians_count == 0:
            status = 0
        else:
            status = int(round(100*float(votes)/float(mozillians_count)))

        return render(request, 'dashboard.html',
                      {'user': user,
                       'status': status,
                       'mozillians': mozillians_data,
                       'countries': COUNTRIES})
    return redirect(main)


def login_failed(request):
    """Redirect to login page on login failure."""
    messages.warning(request, ('Login failed. Please make sure that you '
                               'have an account, and your email '
                               'is verified.'))
    return render(request, 'index.html')


def view_voting(request, slug):
    """View voting and cast a vote view."""
    user = request.user
    if user.is_authenticated():
        mozillian = get_object_or_404(MozillianProfile, slug=slug)
        vote_form = forms.VoteForm(data=request.POST or None,
                                   nominee=mozillian, voter=user)
        # Check POST data and save form
        if vote_form.is_valid():
            if not (Vote.objects
                    .filter(voter=user, nominee=mozillian).exists()):
                Vote.objects.create(voter=user, nominee=mozillian)
            vote_form.save()
            next_entry = mozillian.get_next_entry()
            if next_entry:
                return redirect('voting_view_voting', slug=next_entry.slug)
            return redirect(dashboard)

        return render(request, 'vote.html',
                      {'mozillian': mozillian,
                       'vote_form': vote_form})

    return render(request, 'index.html')
