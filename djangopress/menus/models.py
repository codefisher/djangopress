from django.db import models

class MenuLinkMeta(models.base.ModelBase):
    def __init__(mcs, name, bases, new_attrs):
        models.base.ModelBase.__init__(mcs, name, bases, new_attrs)
        if not hasattr(mcs, 'sub_classes'):
            mcs.sub_classes = {}
        else:
            MenuLink.sub_classes[name] = mcs

class MenuLink(models.Model):

    class_name = models.CharField(max_length=50)
    __metaclass__ = MenuLinkMeta

    def save(self):
        self.class_name = self.__class__.__name__
        super(MenuLink, self).save()

    def get_location(self):
        """Returns the location this menu link should lead too"""
        if self.class_name:
            cls = MenuLink.sub_classes.get(self.class_name)
            if cls:
                link = cls.objects.get(pk=self.pk)
                return link.location

    def __str__(self):
        location = self.get_location()
        if location is not None:
            return location
        return super(MenuLink, self).__str__()

class Menu(models.Model):
    parent_item = models.ForeignKey('MenuItem', null=True, blank=True)
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    parent_menu =  models.ForeignKey('Menu', null=False)
    label = models.CharField(max_length=100)
    link = models.ForeignKey('MenuLink')
    tag = models.CharField(max_length=50, null=True, blank=True)
    index = models.IntegerField()

    def __str__(self):
        return self.label

    def __cmp__(self, other):
        return self.index - other.index

class StaticLink(MenuLink):
    location = models.TextField(blank=True, null=False)

    def get_location(self):
        return self.location

    def __str__(self):
        return self.get_location()