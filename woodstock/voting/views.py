from django.contrib import messages
from django.shortcuts import redirect, render

from models import MozillianProfile, Vote


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
        votes = 0
        for mozillian in mozillians:
            vote = Vote.objects.filter(voter=user, nominee=mozillian)
            if vote:
                mozillians_data[mozillian] = vote[0]
            else:
                mozillians_data[mozillian] = None
        for i in mozillians_data.values():
            if i is not None:
                votes += 1
        status = int(round(100*float(votes)/float(mozillians_count)))

        return render(request, 'dashboard.html',
                      {'user': user,
                       'status': status,
                       'mozillians': mozillians_data})
    return redirect('main')


def login_failed(request):
    """Redirect to login page on login failure."""
    messages.warning(request, ('Login failed. Please make sure that you '
                               'have an account, and your email '
                               'is verified.'))
    return redirect('main')


def view_voting(request, slug):
    """View voting and cast a vote view."""
    user = request.user

    if user.is_authenticated():
        return render(request, 'vote.html')

    return render(request, 'index.html')
