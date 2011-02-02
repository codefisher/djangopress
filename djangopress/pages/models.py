import datetime
from django.db import models
from django.conf import settings
from django.template import Template
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

class PageBlockMeta(models.base.ModelBase):
    def __init__(mcs, name, bases, new_attrs):
        models.base.ModelBase.__init__(mcs, name, bases, new_attrs)
        if not hasattr(mcs, 'sub_classes'):
            mcs.sub_classes = {}
        else:
            PageBlock.sub_classes[name] = mcs

class PageBlock(models.Model):

    class_name = models.CharField(max_length=50, editable=False)
    block_name = models.CharField(max_length=50)
    position = models.IntegerField(blank=True, null=True)
    name = None
    template = None

    __metaclass__ = PageBlockMeta

    def __str__(self):
        return "%s %s" % (self.class_name, self.block_name)

    def save(self):
        self.class_name = self.__class__.__name__
        super(PageBlock, self).save()

    def content(self, context):
        if self.class_name:
            cls = PageBlock.sub_classes.get(self.class_name)
            if cls:
                block = cls.objects.get(pk=self.pk)
                return block.content(context)
        return None

class HTMLBlock(PageBlock):
    name = "HTML"
    data = models.TextField(blank=False, null=False)

    def content(self, context):
        return self.data

class TemplateBlock(PageBlock):
    name = "HTML"
    data = models.TextField(blank=False, null=False)

    def content(self, context):
        t = Template(self.data)
        return t.render(context)

class Page(models.Model):
    PUBLICATION_LEVEL = (
        ('DR', 'Draft'),
        ('PR', 'Pending Review'),
        ('PB', 'Published'),
    )

    VISIBILITY_LEVEL = (
        ('VI', 'Visible'),
        ('PR', 'Private'),
    )

    prepopulated_fields = {
        "slug": ("title", ),
        "meta_page_title": ("title", )
    }

    title = models.CharField(blank=False, max_length=200,
            verbose_name="Page Title")
    sites = models.ManyToManyField(Site)
    template = models.CharField(blank=False, max_length=200,
            choices=settings.PAGES_TEMPLATES)
    blocks = models.ManyToManyField(PageBlock)

    parent = models.ForeignKey("Page", related_name="sub_pages", blank=True, null=True)
    location = models.CharField(max_length=200, db_index=True,
            blank=True, null=True, editable=False)
    override_location = models.CharField(max_length=200, unique=True, blank=True, null=True)
    slug = models.SlugField(blank=False, null=False)

    author = models.ForeignKey(User, editable=False, related_name="pages")
    edited_by = models.ForeignKey(User, editable=False, related_name="edited_pages")
    edited = models.DateTimeField(blank=True,
            auto_now=True, verbose_name="Last Edited", editable=False)
    posted = models.DateTimeField(blank=True, default=datetime.datetime.now,
            verbose_name="Publication Date")

    status = models.CharField(blank=False, max_length=2,
            choices=PUBLICATION_LEVEL, default="DR")
    visibility = models.CharField(blank=False, max_length=2,
            choices=VISIBILITY_LEVEL, default="VI")

    login_required = models.BooleanField(default=False)

    meta_page_title = models.TextField(verbose_name="Page title tag",
            blank=True, null=True)
    meta_keywords = models.TextField(verbose_name="Keywords meta tag",
            blank=True, null=True)
    meta_description = models.TextField(verbose_name="Description meta tag",
            blank=True, null=True)

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"
        unique_together = ("slug", "parent")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.location

    def save(self):
        if self.override_location:
            self.location = self.override_location
        else:
            parent = self.parent.get_absolute_url() if self.parent else "/"
            self.location = "%s%s/" % (parent, self.slug)
        super(Page, self).save()