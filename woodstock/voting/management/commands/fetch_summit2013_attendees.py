import json
import requests
import urllib

from django.core.management.base import BaseCommand
from django.conf import settings

from woodstock.voting.models import MozillianProfile, MozillianGroup

def fetch_summit_attendees():
    """Helper function to fetch summit attendees."""

    MOZILLIANS_URL = settings.MOZILLIANS_URL
    MOZILLIANS_API_URL = settings.MOZILLIANS_API_URL
    MOZILLIANS_APP_KEY = settings.MOZILLIANS_APP_KEY
    MOZILLIANS_APP_NAME = settings.MOZILLIANS_APP_NAME

    data = {'app_name': MOZILLIANS_APP_NAME,
            'app_key': MOZILLIANS_APP_KEY,
            'limit': 200,
            'is_vouched': True}

    MOZILLIANS_API_URL += '?' + urllib.urlencode(data)

    resp = requests.get(MOZILLIANS_API_URL)

    if not resp.status_code == 200:
        raise BadStatusCodeError('Error in HTTP response status')

    content = json.loads(resp.content)
    users = content['objects']

    while content['meta']['next']:
        resp = requests.get(MOZILLIANS_URL + content['meta']['next'])
        print content['meta']['next']

        if not resp.status_code == 200:
            raise BadStatusCodeError('Error in HTTP response status')

        content = json.loads(resp.content)
        users += content['objects']

    summit = []
    for user in users:
        if 'summit2013' in user.get(u'groups', []):
            summit.append(user)

    return summit


class Command(BaseCommand):
    """Management command to fetch Summit attendees from mozillians.org."""

    args = None
    help = 'Fetch Mozilla Summit 2013 attendees from mozillians.org'

    def handle(self, *args, **options):
        """Command handler."""

        attendees = fetch_summit_attendees()
        print "Fetched attendees"
        for user in attendees:
            print user
            groups = []
            for group in user['groups']:
                obj,created = MozillianGroup.objects.get_or_create(name=group)
                groups.append(obj)

            mozillian = MozillianProfile(
                full_name = user['full_name'],
                email = user['email'],
                city = user['city'],
                country = user['country'],
                ircname = user['ircname'],
                avatar_url = user['photo'],
                bio = user['bio'])

            mozillian.save()
            mozillian.tracking_groups = groups
