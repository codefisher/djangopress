
class Profile(object):
    label = None
    show_tab = True
    
    def __init__(self, user):
        self._user = user
        
    def info(self):
        pass
    
    def edit(self, request):
        pass
    
    def admin(self, request):
        pass
    
class ProfileText(object):
    def __init__(self, text):
        self._text = text
        
    def is_text(self):
        return True
    
    def __unicode__(self):
        return self._text

class ProfileRegister(object):

    def __init__(self):
        self._profile = {}
        self._position  = {}

    def __call__(self, name, cls, position=0):
        self._profile[name] = cls
        self._position[name] = position

    def get_profiles(self):
        return self._profile
    
    def get_positions(self):
        return self._position

register = ProfileRegister()

def autodiscover():
    "based on the admin site autodiscover see that for more info"
    import copy
    from django.conf import settings
    try:
        from importlib import import_module
    except:
        from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            before_import_registry = copy.copy(register._profile)
            import_module('%s.profile' % app)
        except:
            register._profile = before_import_registry
            if module_has_submodule(mod, 'profile'):
                raise