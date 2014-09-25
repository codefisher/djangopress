import pytz
import datetime, time
from django.utils import timezone
from django.conf import settings

DEFAULT_LASTSEEN_SESSION_TIMEOUT = 30*60 
LASTSEEN_SESSION_TIMEOUT = getattr(settings, "LASTSEEN_SESSION_TIMEOUT", DEFAULT_LASTSEEN_SESSION_TIMEOUT)

class TimezoneMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            tzname = request.user.profile.timezone
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
            

class LastSeenMiddleware(object):
   
    def now_seconds(self):
        return time.mktime(datetime.datetime.utcnow().timetuple())
            
    def process_response(self, request, response):
        # last_seen is always the last time they visited a page
        # last_seen_session is when this session started.  A new session starts when last_seen is created then LASTSEEN_SESSION_TIMEOUT
        if not hasattr(request, 'session'):
            return
        if request.session.get("last_seen"):
            if (self.now_seconds() - request.session.get("last_seen")) > DEFAULT_LASTSEEN_SESSION_TIMEOUT:
                request.session["last_seen_session"] = request.session.get("last_seen")
        else:
            # the user was not seen before, session starts now
            request.session["last_seen_session"] = self.now_seconds()
        request.session["last_seen"] = self.now_seconds()
        return response
    
def get_last_seen(request):
    if request.session.get("last_seen_session"):
        return datetime.datetime.utcfromtimestamp(request.session.get("last_seen_session"))
    return datetime.datetime.utcnow()