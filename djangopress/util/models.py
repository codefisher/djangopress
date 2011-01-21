from django.db import models

# Create your models here.

class PropertyMeta(models.base.ModelBase):
    def __init__(mcs, name, bases, new_attrs):
        models.base.ModelBase.__init__(mcs, name, bases, new_attrs)
        if not hasattr(mcs, 'sub_classes'):
            mcs.sub_classes = {}
        else:
            Property.sub_classes[name] = mcs

class Property(models.Model):

    class_name = models.CharField(max_length=50, editable=False)
    property = models.CharField(max_length=50)

    __metaclass__ = PropertyMeta

    def save(self):
        self.class_name = self.__class__.__name__
        super(Property, self).save()

    def value(self):
        if self.class_name:
            cls = Property.sub_classes.get(self.class_name)
            if cls:
                property = cls.objects.get(pk=self.pk)
                return property.value()
        raise NotImplementedError

class CharProperty(Property):

    property_value = models.CharField(max_length=255)

    def value(self):
        return self.property_value

class IntProperty(Property):

    property_value = models.IntegerField()

    def value(self):
        return self.property_value