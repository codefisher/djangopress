import datetime

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.pages.blocks import PageBlock

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
    blocks = models.ManyToManyField(PageBlock, related_name="pages", blank=True, null=True)

    parent = models.ForeignKey("Page", related_name="sub_pages", blank=True, null=True)
    location = models.CharField(max_length=200, db_index=True,
            blank=True, null=True, editable=False)
    override_location = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=False, null=False)

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

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"
        unique_together = ("slug", "parent")

    def __unicode__(self):
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