from djangopress.pages.views import show_page
from django.http import Http404
from django.conf import settings
from djangopress.core import dynamic

class PagesMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        try:
            for func, mod in dynamic.register.get_modules():
                pass
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response