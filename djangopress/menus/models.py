from django.db import models
from djangopress.menus.menu import register as menu_register

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class_tag = models.CharField(max_length=100, null=True, blank=True)
    renderer = models.CharField(max_length=100, default="default")
    
    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    label = models.CharField(max_length=100)
    link = models.CharField(max_length=255, null=True, blank=True)
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    parent = models.ForeignKey('MenuItem', null=True, blank=True, on_delete=models.CASCADE)
    
    index = models.IntegerField(default=0)
    
    id_tag = models.CharField(max_length=100, null=True, blank=True)
    class_tag = models.CharField(max_length=100, null=True, blank=True)
    renderer = models.CharField(max_length=100, default="default", choices=list(menu_register.list_all().items()))
    
    def __str__(self):
        return "%s (#%s)" % (self.label, self.pk)

from djangopress.menus.menu import autodiscover

autodiscover()