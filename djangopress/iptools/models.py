import os
from django.db import models
import geoip2.database
from django.conf import settings


DEFAULT_DATABASE_FILE = os.path.join(settings.BASE_DIR, '..', 'db', 'GeoLite2-City.mmdb')
DATABASE_FILE = getattr(settings, "GEOLITE2_DATABASE_FILE", DEFAULT_DATABASE_FILE)

# this expensive so putting it here is how we make it run once at startup
reader = geoip2.database.Reader(DATABASE_FILE)