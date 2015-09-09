from django.conf.urls import *

urlpatterns = patterns(
    'woodstock.voting.views',
    url(r'^$', 'dashboard', name='voting_dashboard'),
)
