class MenusRegister(object):

    def __init__(self):
        self._renderer = {}

    def __call__(self, name, cls, position=0):
        self._renderer[name] = cls

    def get_renderer(self, name):
        return self._renderer.get(name)

register = MenusRegister()

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
            before_import_registry = copy.copy(register._renderer)
            import_module('%s.menus' % app)
        except:
            register._renderer = before_import_registry
            if module_has_submodule(mod, 'menus'):
                raise
            