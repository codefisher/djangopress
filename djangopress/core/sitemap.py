
class SitemapRegister(object):

    def __init__(self):
        self._sitemaps = {}

    def __call__(self, name, cls):
        self._sitemaps[name] = cls

    def get_sitemaps(self):
        return self._sitemaps

register = SitemapRegister()

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
            before_import_registry = copy.copy(register._sitemaps)
            import_module('%s.sitemaps' % app)
        except:
            register._sitemaps = before_import_registry
            if module_has_submodule(mod, 'sitemaps'):
                raise
