from django.db import models

# Create your models here.

class LinkMeta(models.base.ModelBase):
    def __init__(mcs, name, bases, new_attrs):
        models.base.ModelBase.__init__(mcs, name, bases, new_attrs)
        if not hasattr(mcs, 'sub_classes'):
            mcs.sub_classes = {}
        else:
            Link.sub_classes[name] = mcs

def get_child_func(func):
    def _get_child_func(self):
        if self.class_name:
            if self.link:
                return func(self, self.link)
            else:
                cls = Link.sub_classes.get(self.class_name)
                if cls:
                    self.link = cls.objects.get(pk=self.pk)
                    return func(self, self.link)
        return None
    return _get_child_func

class Link(models.Model):

    class_name = models.CharField(max_length=50, editable=False, db_index=True)
    __metaclass__ = LinkMeta

    def __init__(self, *args, **kargs):
        self.link = None
        super(Link, self).__init__(*args, **kargs)

    def save(self):
        self.class_name = self.__class__.__name__
        super(Link, self).save()

    @get_child_func
    def get_absolute_url(self, link):
        """Returns the location this link should lead too"""
        return link.get_absolute_url()

    @get_child_func
    def label(self, link):
        """Returns the label of the link"""
        return link.label()

    def __str__(self):
        location = self.get_absolute_url()
        if location is not None:
            return location
        return super(Link, self).__str__()

class StaticLink(Link):
    location = models.TextField(blank=True, null=False)
    label_text = models.CharField(max_length=100, blank=True, null=False)

    def label(self):
        return self.label_text

    def get_absolute_url(self):
        return self.location