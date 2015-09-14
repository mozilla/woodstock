import logging
import requests
import urllib

from django.conf import settings

from django_countries.data import COUNTRIES

from models import MozillianGroup, MozillianProfile


logger = logging.getLogger(__name__)


API_RESULTS_LIMIT = 200
MOZILLIANS_API_URL = settings.MOZILLIANS_API_URL


def get_mozillian_by_username(username):
    """Helper method to query API."""
    data = {
        'app_name': settings.MOZILLIANS_APP_NAME,
        'app_key': settings.MOZILLIANS_APP_KEY,
        'limit': API_RESULTS_LIMIT,
        'username': username
    }

    url = MOZILLIANS_API_URL + '?' + urllib.urlencode(data)
    resp = requests.get(url)

    if not resp.status_code == 200:
        logger.error('Reponse status: {}'.format(resp.status_code))
        return None

    content = resp.json()
    return content['objects'][0]


def update_mozillian_profiles(queryset=None):
    """Sync MozillianProfile objects with mozillians.org"""

    if not queryset:
        queryset = MozillianProfile.objects.all()

    for mozillian in queryset:
        data = get_mozillian_by_username(mozillian.mozillian_username)

        if not data:
            continue

        country = COUNTRIES.get(data['country'].upper(), '').capitalize()
        mozillian.full_name = data['full_name']
        mozillian.email = data['email']
        mozillian.city = data['city']
        mozillian.country = country
        mozillian.ircname = data['ircname']
        mozillian.avatar_url = data['photo']
        mozillian.bio = data['bio']
        mozillian.save()

        mozillian.tracking_groups.clear()
        groups = []
        for group in data['groups']:
            obj, created = MozillianGroup.objects.get_or_create(name=group)
            groups.append(obj)

        mozillian.tracking_groups = groups
        logger.debug('Mozillian succesfully updated.')


def get_object_or_none(model_class, **kwargs):
    """Identical to get_object_or_404, except instead of returning Http404,
    this returns None.

    """
    try:
        return model_class.objects.get(**kwargs)
    except (model_class.DoesNotExist, model_class.MultipleObjectsReturned):
        return None
