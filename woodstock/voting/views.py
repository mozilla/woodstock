from django.contrib import messages
from django.shortcuts import redirect, render


def main(request):
    """Main page view."""
    return render(request, 'index.html')


#TODO check if user is authenticated
def dashboard(request):
    return render(request, 'dashboard.html')


def login_failed(request):
    """Redirect to login page on login failure."""
    messages.warning(request, ('Login failed. Please make sure that you '
                               'have an account ,and your email '
                               'is verified.'))
    return redirect('main')
