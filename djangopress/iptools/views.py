from django.shortcuts import render
from djangopress.iptools.models import reader
from django.conf import settings
from geoip2.errors import AddressNotFoundError
import os

DEFAULT_FLAG_FOLDER = os.path.join(settings.BASE_DIR, '..', 'www', 'static', 'images', 'flags')
FLAG_FOLDER = getattr(settings, "IPTOOLS_FLAG_FOLDER", DEFAULT_FLAG_FOLDER)

DEFAULT_FLAG_WEB_FOLDER = settings.STATIC_URL + "images/flags/"
FLAG_WEB_FOLDER = getattr(settings, "IPTOOLS_FLAG_WEB_FOLDER", DEFAULT_FLAG_WEB_FOLDER)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR')

def get_time_zone(ip_address):
    try:
        response = reader.city(ip_address)
        return response.location.time_zone
    except AddressNotFoundError:
        return None

def get_request_time_zone(request):
    return get_time_zone(get_client_ip(request))


def get_ip_country_flag(ip_address):
    try:
        response = reader.city(ip_address)
        iso_code = response.country.iso_code
    except AddressNotFoundError:
        return None
    if os.path.isfile(os.path.join(FLAG_FOLDER, '%s.png' % iso_code.lower())):
        return FLAG_WEB_FOLDER + '%s.png' % iso_code.lower()
    else:
        return None