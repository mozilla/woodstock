from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

urlpatterns = patterns('',
    # BrowserId
    url(r'^browserid/', include('django_browserid.urls')),
    # Login/Logout
    url(r'^login/failed/$', 'woodstock.voting.views.login_failed',
        name='login_failed'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url('^login/$', 'woodstock.voting.views.login_required_view',
        name='login_required'),
    # Voting urls
    url(r'^dashboard/', include('woodstock.voting.voting_urls')),
    url(r'^v/', include('woodstock.voting.v_urls')),
    # Admin:
    url(r'^admin/', include(admin.site.urls)),
    # Main Page
    url(r'^$', 'woodstock.voting.views.main', name='main'),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    static_url = settings.STATIC_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % static_url, 'django.views.static.serve',
            {'document_root': './woodstock/voting/static/'}),
    )
