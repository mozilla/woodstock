import logging
import requests
import urllib

from django.conf import settings

from django_countries.data import COUNTRIES

from models import MozillianGroup, MozillianProfile

logger = logging.getLogger(__name__)


def update_mozillian_profiles():
    """Sync MozillianProfile objects with mozillians.org"""
    mozillians = MozillianProfile.objects.all()

    MOZILLIANS_API_URL = settings.MOZILLIANS_API_URL
    data = {'app_name': settings.MOZILLIANS_APP_NAME,
            'app_key': settings.MOZILLIANS_APP_KEY,
            'limit': 200}

    for mozillian in mozillians:
        data['mozillian_username'] = mozillian.username

        url = MOZILLIANS_API_URL + '?' + urllib.urlencode(data)
        resp = requests.get(url)

        if not resp.status_code == 200:
            logger.error('Reponse status: {}'.format(resp.status_code))
            continue

        content = resp.json()
        m = content['objects'][0]

        mozillian.full_name = m['full_name']
        mozillian.email = m['email']
        mozillian.city = m['city']
        mozillian.country = (COUNTRIES
                             .get(m['country'].upper(), '').capitalize())
        mozillian.ircname = m['ircname']
        mozillian.avatar_url = m['photo']
        mozillian.bio = m['bio']
        mozillian.save()

        mozillian.tracking_groups.clear()
        groups = []
        for group in m['groups']:
            obj, created = MozillianGroup.objects.get_or_create(name=group)
            groups.append(obj)

        mozillian.tracking_groups = groups
        logger.debug('Mozillian succesfully updated.')
