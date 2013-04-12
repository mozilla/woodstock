from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

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
    mozillian = get_object_or_404(MozillianProfile, slug=slug)
    if user.is_authenticated():

        # Mozillian data for vote page
        args = {}
        args['name'] = mozillian.full_name
        args['email'] = mozillian.email
        args['city'] = mozillian.city
        args['country'] = mozillian.country
        args['irc'] = mozillian.ircname
        args['groups'] = mozillian.tracking_groups.all()
        args['bio'] = mozillian.bio
        args['avatar_url'] = mozillian.avatar_url

        #TODO: previous, next
        args['previous'] =(mozillian.get_previous_entry()).slug
        args['next'] = (mozillian.get_next_entry()).slug
        #TODO: bugzilla activity
        #TODO: mozillians profile

        return render(request, 'vote.html', args)

    return render(request, 'index.html')
