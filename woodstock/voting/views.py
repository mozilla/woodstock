from django.shortcuts import render


#TODO check if user is authenticated
def list_votings(request, slug):
    return render(request, 'list_votings.html')
