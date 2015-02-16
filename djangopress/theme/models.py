from django.db import models, OperationalError

from django.conf import settings
from importlib import import_module
from django.utils.module_loading import module_has_submodule

class ThemeLibrary(object):
    themes = {}
    active = None
        
    @classmethod
    def add(cls, theme):
        try:
            if not Theme.objects.filter(name=theme['name']):
                active = not Theme.objects.all().count()
                theme_obj = Theme(name=theme['name'], slug=theme['slug'], display_name=theme['display_name'], active=active)
                theme_obj.save()
            cls.themes[theme['name']] = theme
        except OperationalError:
            pass # will happen when running makemigrations
        
    @classmethod
    def get_active(cls):
        if not cls.active:
            cls.active = Theme.objects.get(active=True)
        return cls.active
        
def autodiscover():
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            module = import_module('%s.theme' % app)
            # needed because we seem to get mutiple Library
            # objects in memory and this makes them all
            # form one
            ThemeLibrary.add(module.theme_meta)
        except:
            if module_has_submodule(mod, 'theme'):
                raise
            
class Theme(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=False)
    display_name = models.CharField(max_length=100)
    
    def save(self):
        if self.active:
            Theme.objects.exclude(pk=self.pk).update(active=False)
            ThemeLibrary.active = self
        super(Theme, self).save()