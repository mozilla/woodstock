import requests
import urllib

from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from django_countries import data
from woodstock.voting.models import MozillianProfile, MozillianGroup


def BadStatusCodeError(Exception):
    """Something went totally wrong."""
    pass


def fetch_mozillians_by_group(group):
    """Helper function to fetch users in a mozillians.org group."""

    MOZILLIANS_URL = settings.MOZILLIANS_URL
    MOZILLIANS_API_URL = settings.MOZILLIANS_API_URL
    data = {'app_name': settings.MOZILLIANS_APP_NAME,
            'app_key': settings.MOZILLIANS_APP_KEY,
            'limit': 200,
            'is_vouched': True,
            'groups': group}

    MOZILLIANS_API_URL += '?' + urllib.urlencode(data)

    url = MOZILLIANS_API_URL
    mozillians = []
    while True:
        resp = requests.get(url)

        if not resp.status_code == 200:
            raise ValueError('Error in HTTP response status')

        content = resp.json()
        for user in content['objects']:
            mozillians.append(user)

        if not content['meta'].get('next', ''):
            break

        url = MOZILLIANS_URL + content['meta']['next']

    return mozillians


class Command(BaseCommand):
    help = 'Fetch candidates by mozillians.org group.'

    option_list = BaseCommand.option_list + (
        make_option('-g', '--group',
                    action='store',
                    dest='group',
                    default=None,
                    help='mozillians.org group'),
    )

    def handle(self, *args, **options):
        """Command handler."""

        if not options['group']:
            raise ValueError('mozillians.org group not given')

        candidates = fetch_mozillians_by_group(options['group'])
        print('Fetching candidates...')
        for user in candidates:
            groups = []
            for group in user['groups']:
                obj, created = MozillianGroup.objects.get_or_create(name=group)
                groups.append(obj)

            mozillian = MozillianProfile(
                full_name=user['full_name'],
                email=user['email'],
                username=user['username'],
                city=user['city'],
                country=(data.COUNTRIES
                         .get(user['country'].upper(), '').capitalize()),
                ircname=user['ircname'],
                avatar_url=user['photo'],
                bio=user['bio'])

            mozillian.save()
            mozillian.tracking_groups = groups
            print('Users successfully imported.')

        print('{0} candidates fetched'.format(len(candidates)))
