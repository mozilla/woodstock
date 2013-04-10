from django.conf.urls.defaults import *

urlpatterns = patterns('woodstock.voting.views',
    url(r'^$', 'list_votings', name='voting_list_votings'),
)
