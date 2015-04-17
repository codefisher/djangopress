MIDDLEWARE_CLASSES = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'codefisher_apps.reverseproxy.middleware.ProxyMiddleware',
    'djangopress.pages.middleware.PagesMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'djangopress.accounts.middleware.TimezoneMiddleware',
    'djangopress.accounts.middleware.LastSeenMiddleware',
    'codefisher_apps.online_status.middleware.OnlineStatusMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

TITLE_FORMAT = "%s :: %s"