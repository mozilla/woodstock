# Django settings for woodstock project.
import dj_database_url
import os

from decouple import Csv, config

DEBUG = config('DEBUG', cast=bool)
TEMPLATE_DEBUG = config('TEMPLATE_DEBUG', default=DEBUG, cast=bool)

DATABASES = {
    'default': config('DATABASE_URL', cast=dj_database_url.parse)
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = config('TIME_ZONE', default='UTC')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = config('USE_I18N', default=True, cast=bool)

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = config('USE_L10N', default=True, cast=bool)

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = config('USE_TZ', default=True, cast=bool)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = config('MEDIA_URL', '/media/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static'))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = config('STATIC_URL', '/static/')

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'woodstock.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'woodstock.wsgi.application'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django_browserid',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    'woodstock.voting',
    'import_export',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages'
)

# Django browserid authentication backend
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.BrowserIDBackend',
)

# Uncomment the following line for local development, or BrowserID
# will fail to log you in.
SITE_URL = config('SITE_URL')

# Do not create account for new users.
BROWSERID_CREATE_USER = False
BROWSERID_AUDIENCES = config('BROWSERID_AUDIENCES', cast=Csv())
BROWSERID_VERIFY_CLASS = 'woodstock.voting.views.BrowserIDVerify'

# Path to redirect to on successful login.
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/events/'

# Path to redirect to on unsuccessful login attempt.
LOGIN_REDIRECT_URL_FAILURE = '/'
LOGOUT_REDIRECT_URL = '/'

MOZILLIANS_URL = "https://mozillians.org"
MOZILLIANS_API_URL = "https://mozillians.org/api/v1/users/"
REPS_API_URL = "https://reps.mozilla.org/api/v1/rep/"

# Replace with your mozillians API credentials
MOZILLIANS_APP_KEY = config('MOZILLIANS_APP_KEY', default=None)
MOZILLIANS_APP_NAME = config('MOZILLIANS_APP_NAME', default=None)

LOGIN_URL = '/login/'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

try:
    from local_settings import *  # noqa
except:
    pass
