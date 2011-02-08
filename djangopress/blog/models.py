import datetime
from django.db import models
from django.core.urlresolvers import reverse
from djangopress.core.links.models import Link
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, unique=True)
    blog = models.ForeignKey("Blog", related_name="tags")

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        unique_together = ("slug", "blog")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog-tag", kwargs={"slug": self.slug})

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True,
            related_name="child_categories")
    blog = models.ForeignKey("Blog", related_name="categories")

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        unique_together = ("slug", "blog")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog-category", kwargs={"slug": self.slug})

class Blog(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    tagline = models.TextField(blank=True, null=False)
    sites = models.ManyToManyField(Site)

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {}
        if self.slug:
            kwargs["blog"] = self.slug
        return reverse("blog-index", kwargs=kwargs)

class Entry(models.Model):
    PUBLICATION_LEVEL = (
        ('DR', 'Draft'),
        ('PR', 'Pending Review'),
        ('PB', 'Published'),
    )

    VISIBILITY_LEVEL = (
        ('VI', 'Visible'),
        ('PR', 'Private'),
        #('PP', 'Password Protected'),
    )

    prepopulated_fields = {
        "slug": ("title", )
    }

    blog = models.ForeignKey(Blog, related_name="entries")
    title = models.CharField(blank=False, max_length=200,
            verbose_name="Post Title")
    slug = models.SlugField(blank=False, unique_for_date='posted')
    body = models.TextField(blank=False, verbose_name="Post Contents")
    # change to user profile
    author = models.ForeignKey(User, related_name="blog_entries")
    edited_by = models.ForeignKey(User, editable=False, related_name="blog_edited_entries")
    edited = models.DateTimeField(blank=True,
            auto_now=True, verbose_name="Last Edited", editable=False)
    posted = models.DateTimeField(blank=True, default=datetime.datetime.now,
            verbose_name="Publication Date")
    status = models.CharField(blank=False, max_length=2,
            choices=PUBLICATION_LEVEL, default="DR")
    sticky = models.BooleanField(default=False)
    visibility = models.CharField(blank=False, max_length=2,
            choices=VISIBILITY_LEVEL, default="VI")
    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"

    @staticmethod
    def get_entries(blog=None, sorted=True):
        entry_list = Entry.objects.select_related('blog', 'author').filter(status="PB", visibility="VI")
        if blog is not None:
            entry_list.filter(blog=blog)
        if sorted:
            return entry_list.order_by('-sticky', '-posted')
        return entry_list

    def __str__(self):
        return self.title

    def save(self):
        super(Entry, self).save()

    def get_absolute_url(self):
        kwargs = {
            "year": self.posted.year,
            "month": "%02d" % self.posted.month,
            "day": "%02d" % self.posted.day,
            "slug": self.slug,
        }
        if self.blog.slug:
            kwargs["blog"] = self.blog.slug
        return reverse("blog-post", kwargs=kwargs)

class EntryLink(Link):
    entry = models.ForeignKey(Entry, null=False, blank=False, related_name="links")

    def label(self):
        return self.entry.title

    def get_absolute_url(self):
        return self.entry.get_absolute_url()

from django.contrib import databrowse
databrowse.site.register(Entry)
