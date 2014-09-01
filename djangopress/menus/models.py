from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class_tag = models.CharField(max_length=100, null=True, blank=True)
    renderer = models.CharField(max_length=100, default="default")
    
    def __unicode__(self):
        return self.name
    
class MenuItem(models.Model):
    label = models.CharField(max_length=100)
    link = models.CharField(max_length=255, null=True, blank=True)
    
    menu = models.ForeignKey(Menu)
    parent = models.ForeignKey('MenuItem', null=True, blank=True)
    
    index = models.IntegerField(default=0)
    
    id_tag = models.CharField(max_length=100, null=True, blank=True)
    class_tag = models.CharField(max_length=100, null=True, blank=True)
    renderer = models.CharField(max_length=100, default="default")
    
    def __unicode__(self):
        return "%s %s" % (self.label, self.pk)
    