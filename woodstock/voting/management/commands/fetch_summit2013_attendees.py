import requests
import urllib

from django.core.management.base import BaseCommand
from django.conf import settings

from django_countries import countries
from woodstock.voting.models import MozillianProfile, MozillianGroup


def BadStatusCodeError(Exception):
    """Something went totally wrong."""
    pass


def fetch_summit_attendees():
    """Helper function to fetch summit attendees."""

    MOZILLIANS_URL = settings.MOZILLIANS_URL
    MOZILLIANS_API_URL = settings.MOZILLIANS_API_URL
    summit = []
    data = {'app_name': settings.MOZILLIANS_APP_NAME,
            'app_key': settings.MOZILLIANS_APP_KEY,
            'limit': 200,
            'is_vouched': True}

    MOZILLIANS_API_URL += '?' + urllib.urlencode(data)

    url = MOZILLIANS_API_URL
    while True:
        resp = requests.get(url)

        if not resp.status_code == 200:
            raise ValueError('Error in HTTP response status')

        content = resp.json()
        for user in content['objects']:
            if 'summit2013' in user.get(u'groups', []):
                summit.append(user)

        if not content['meta'].get('next', ''):
            break

        url = MOZILLIANS_URL + content['meta']['next']

    return summit


class Command(BaseCommand):
    """Management command to fetch Summit attendees from mozillians.org."""

    args = None
    help = 'Fetch Mozilla Summit 2013 attendees from mozillians.org'

    def handle(self, *args, **options):
        """Command handler."""

        attendees = fetch_summit_attendees()
        print('Fetching attendees')
        for user in attendees:
            groups = []
            for group in user['groups']:
                obj, created = MozillianGroup.objects.get_or_create(name=group)
                groups.append(obj)

            mozillian = MozillianProfile(
                full_name=user['full_name'],
                email=user['email'],
                city=user['city'],
                country=(countries.OFFICIAL_COUNTRIES
                         .get(user['country'].upper(), '').capitalize()),
                ircname=user['ircname'],
                avatar_url=user['photo'],
                bio=user['bio'])

            mozillian.save()
            mozillian.tracking_groups = groups
            print('Users successfully imported.')
