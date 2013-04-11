from django.conf.urls.defaults import *

urlpatterns = patterns('woodstock.voting.views',
    url(r'^(?P<slug>[a-z0-9-]+)/$', 'view_voting',
        name='voting_view_voting')
)
