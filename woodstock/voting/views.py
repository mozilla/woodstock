from django.contrib import messages
from django.shortcuts import redirect, render

from models import MozillianProfile


def main(request):
    """Main page view."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    else:
        return render(request, 'index.html')


def dashboard(request):
    user = request.user
    if user.is_authenticated():
        mozillians = MozillianProfile.objects.all()
        return render(request, 'dashboard.html',
                      {'user': user,
                       'mozillians': mozillians})
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
