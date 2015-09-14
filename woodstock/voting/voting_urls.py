from django.conf.urls import *

urlpatterns = patterns(
    'woodstock.voting.views',
    url(r'^events/$', 'events', name='voting_events'),
    url(r'^dashboard/$', 'dashboard', name='voting_dashboard'),
)
