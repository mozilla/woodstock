from django.contrib import messages
from django.shortcuts import redirect, render


def main(request):
    """Main page view."""
    if request.user.is_authenticated():
        return redirect(dashboard)
    else:
        return render(request, 'index.html')


def dashboard(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard.html')
    else:
        return redirect(main)


def login_failed(request):
    """Redirect to login page on login failure."""
    messages.warning(request, ('Login failed. Please make sure that you '
                               'have an account, and your email '
                               'is verified.'))
    return render(request, 'index.html')
