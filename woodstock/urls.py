from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # BrowserId
    url(r'^browserid/', include('django_browserid.urls')),
    # Voting urls
    url(r'^', include('woodstock.voting.voting_urls')),
    url(r'^v', include('woodstock.voting.v_urls')),

    # Admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', TemplateView.as_view(template_name="index.html")),
    (r'^dashboard/', TemplateView.as_view(template_name="dashboard.html")),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
