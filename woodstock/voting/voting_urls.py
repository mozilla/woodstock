from django.conf.urls.defaults import *

urlpatterns = patterns('woodstock.voting.views',
    url(r'^$', 'dashboard', name='voting_dashboard'),
)
