from django.conf.urls import *

urlpatterns = patterns(
    'woodstock.voting.views',
    url(r'^(?P<id>[0-9]+)/$', 'view_voting',
        name='voting_view_voting')
)
