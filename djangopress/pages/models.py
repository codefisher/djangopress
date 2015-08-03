import datetime
import time

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.pages.render import register as render_register

class PageTemplate(models.Model):
    name = models.CharField(blank=False, max_length=200)
    template = models.CharField(blank=False, max_length=200,
            help_text="The path to any template file accessible to the template loader")
    
    def __unicode__(self):
        return self.name

def page_file_path(instance, filename):
    if instance.pk:
        return ("pages/{0}/{1}-{2}".format(time.strftime("%y/%m"), instance.pk, filename.lower()))
    return ("pages/{0}/{1}".format(time.strftime("%y/%m"), filename.lower()))

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
    template = models.ForeignKey(PageTemplate, blank=True, null=True)

    parent = models.ForeignKey("Page", related_name="sub_pages", blank=True, null=True)
    location = models.CharField(max_length=200, unique=True,
            blank=True, null=True, editable=False)
    override_location = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=False, null=False)
    image = models.ImageField(upload_to=page_file_path, blank=True, null=True)

    author = models.ForeignKey(User, editable=False, related_name="pages")
    edited_by = models.ForeignKey(User, editable=False, related_name="edited_pages")
    edited = models.DateTimeField(blank=True,
            auto_now=True, verbose_name="Last Edited", editable=False)
    posted = models.DateTimeField(blank=True, default=datetime.datetime.now,
            verbose_name="Publication Date", editable=False)

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
    head_tags = models.TextField(verbose_name="Extra tags to be added to the page header",
            blank=True, null=True)

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"
        unique_together = ("slug", "parent")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.location

    def save(self, *args, **kwargs):
        if self.override_location:
            self.location = self.override_location
        else:
            parent = self.parent.get_absolute_url() if self.parent else "/"
            self.location = "%s%s/" % (parent, self.slug)
        super(Page, self).save(*args, **kwargs)
        
class PageBlock(models.Model):
    block_name = models.CharField(max_length=50, db_index=True, editable=True,
                                  default='content')
    position = models.IntegerField(blank=True, null=True)
    block_id = models.CharField(blank=True, null=True, max_length=50, db_index=True, editable=True,
            help_text="Name used to refer to the block in templates", verbose_name="Id")
    data = models.TextField(blank=True, verbose_name="Content")
    render = models.CharField(max_length=30, choices=render_register.choices(),
                              default='extended_html')
    page = models.ForeignKey(Page, null=True, blank=True, related_name="blocks")

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        if self.page:
            return "%s %s %s" % (self.block_name, self.position, self.page.get_absolute_url())
        return "%s %s" % (self.block_name, self.position)

    def save(self, *args, **kwargs):
        if not hasattr(self, "position") or not self.position:
            self.position = 1
        super(PageBlock, self).save(*args, **kwargs)

    def content(self, context=None):
        return render_register.render(self, self.render, self.data, context)