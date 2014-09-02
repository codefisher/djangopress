# Django settings for codefisher project.

import os
BASE_DIR = os.path.realpath(os.path.dirname(__file__))

INTERNAL_IPS = (
    '127.0.0.1',
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

if DEBUG == True:
    # only during development for warnings of things that are going to be removed
    import warnings
    #warnings.simplefilter('error', DeprecationWarning)
    #warnings.simplefilter('error', PendingDeprecationWarning)

ADMINS = (
    ('Michael Buckley', 'support@codefisher.org'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR, '..', 'sqlite.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Brisbane'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'www', 'media')
MEDIA_UPLOAD = os.path.join(MEDIA_ROOT, "uploads")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
    #)),
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'codefisher_apps.middleware.PagesMiddleware',
    'djangopress.pages.middleware.PagesMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'online_status.middleware.OnlineStatusMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    #'codefisher_apps.pun.middle.ProfileMiddleware',
)

ROOT_URLCONF = 'djangopress.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'templates'),
)

TITLE_FORMAT = "%s :: %s"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'django.contrib.markup',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    # 3rd party apps
#    'south',
    #'django_extensions', # only use during testing
    #'online_status',
    'debug_toolbar',
    # djangopress
    'djangopress.core.format',
    'djangopress.blog',
    'djangopress.menus',
    'djangopress.core',
    'djangopress.accounts',
    'djangopress.pages',
    'djangopress.forum',
    'djangopress.donate',
    'paypal.standard.ipn',
    'djangopress.contact',
    'codefisher_apps.svn_xslt',
)

PAYPAL_RECEIVER_EMAIL = "paypal-foo@codefisher.org "
PAYPAL_TEST = False

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages"
)


AUTH_PROFILE_MODULE = 'accounts.UserProfile'

PAGES_TEMPLATES = (
    ('pages/base.html', 'default'),
    ('pages/home.html', 'home'),
)

from local_settings import *
