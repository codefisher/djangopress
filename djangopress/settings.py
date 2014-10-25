# Django settings for codefisher project.

import os
BASE_DIR = os.path.realpath(os.path.dirname(__file__))

INTERNAL_IPS = (
    '127.0.0.1',
)

ADMINS = (
    ('Michael Buckley', 'support@codefisher.org'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC' #None

USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'www', 'media')
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'www', 'static_files')
MEDIA_UPLOAD = MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

MIDDLEWARE_CLASSES = (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'codefisher_apps.reverseproxy.middleware.ProxyMiddleware',
    'djangopress.pages.middleware.PagesMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'djangopress.accounts.middleware.TimezoneMiddleware',
    'djangopress.accounts.middleware.LastSeenMiddleware',
    'codefisher_apps.online_status.middleware.OnlineStatusMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'djangopress.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'templates'),
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

TITLE_FORMAT = "%s :: %s"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    # djangopress
    'djangopress.core.format',
    'djangopress.blog',
    'djangopress.menus',
    'djangopress.core',
    'djangopress.accounts',
    'djangopress.theme',
    'djangopress.pages',
    'djangopress.forum',
    'djangopress.donate',
    'djangopress.iptools',
    'paypal.standard',
    'paypal.standard.ipn',
    'djangopress.contact',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

PAYPAL_RECEIVER_EMAIL = "paypal@codefisher.org"
PAYPAL_TEST = False

from local_settings import *
