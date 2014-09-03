from django.conf import settings
try:
    from importlib import import_module
except:
    from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
import nodes

for app in settings.INSTALLED_APPS:
    mod = import_module(app)
    try:
        module = import_module('%s.format_tags' % app)
        # needed because we seem to get mutiple Library
        # objects in memory and this makes them all
        # form one
        nodes.Library.tags.update(module.library.tags)
    except:
        if module_has_submodule(mod, 'format_tags'):
            raise