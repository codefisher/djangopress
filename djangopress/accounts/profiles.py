
class Profile(object):
    def __init__(self, user):
        self._user = user
    
    def info(self):
        pass
    
    def edit(self, request):
        pass
    
    def admin(self, request):
        pass

class ProfileRegister(object):

    def __init__(self):
        self._profile = {}

    def __call__(self, name, cls):
        self._profile[name] = cls

    def get_profiles(self):
        return self._profile

register = ProfileRegister()

def autodiscover():
    "based on the admin site autodiscover see that for more info"
    import copy
    from django.conf import settings
    from importlib import import_module
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