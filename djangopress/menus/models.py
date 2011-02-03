from django.db import models
from djangopress.core.links.models import Link

class Menu(models.Model):
    parent_item = models.ForeignKey('MenuItem', null=True, blank=True, related_name="child")
    name = models.CharField(max_length=30, primary_key=True)

    def save(self):
        if self.parent_item:
            self.parent_item.has_child = True
            self.parent_item.save()
        super(Menu, self).save()

    def delete(self):
        if self.parent_item:
            self.parent_item.has_child = False
            self.parent_item.save()
        super(Menu, self).delete()

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    parent_menu =  models.ForeignKey('Menu', null=False, related_name="children")
    link = models.ForeignKey(Link)
    tag = models.CharField(max_length=50, null=True, blank=True)
    index = models.IntegerField()
    has_child = models.BooleanField(default=False)

    def __str__(self):
        return self.link.label()

    def __cmp__(self, other):
        return self.index - other.index