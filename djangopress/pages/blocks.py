from django.db import models
from django.template import Template
from django import forms
from djangopress.core.format import Library as FormatLibrary

class PageBlockMeta(models.base.ModelBase):
    def __init__(mcs, name, bases, new_attrs):
        models.base.ModelBase.__init__(mcs, name, bases, new_attrs)
        if not hasattr(mcs, 'sub_classes'):
            mcs.sub_classes = {}
        else:
            PageBlock.sub_classes[name] = mcs

class PageBlock(models.Model):
    class_name = models.CharField(max_length=50, editable=False, db_index=True)
    block_name = models.CharField(max_length=50, db_index=True)
    position = models.IntegerField(blank=True, null=True)
    block_id = models.CharField(blank=True, null=True, max_length=50, db_index=True,
            help_text="Name used to refer to the block in templates", verbose_name="Id")
    name = "Page Block"
    template = None
    form = None

    __metaclass__ = PageBlockMeta

    class Meta:
        ordering = ['position']

    def __str__(self):
        if self.name:
            return "%s %s %s %s" % (self.name, self.class_name, self.block_name, self.position)
        return "%s %s %s" % (self.class_name, self.block_name, self.position)

    def save(self):
        self.class_name = self.__class__.__name__
        if not hasattr(self, "position") or not self.position:
            self.position = 1
        super(PageBlock, self).save()

    def get_child(self):
        if self.class_name:
            cls = PageBlock.sub_classes.get(self.class_name)
            if cls:
                return cls.objects.get(pk=self.pk)
        return None

    def content(self, context):
        block = self.get_child()
        if block:
            return block.content(context)
        return None


class TextBlock(PageBlock):
    name = "Text"
    data = models.TextField(blank=True)
    format = models.CharField(max_length=30, choices=FormatLibrary.choices(False))

    def content(self, context):
        return FormatLibrary.format(self.format, self.data, False, context=context)

class TextForm(forms.ModelForm):
    template = None

    class Meta:
        model = TextBlock
        widgets = {
            'block_name': forms.HiddenInput()
        }
TextBlock.form = TextForm