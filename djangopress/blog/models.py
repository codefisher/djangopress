import datetime
from django.db import models
from django.core.urlresolvers import reverse
from djangopress.menus.models import MenuLink

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=False)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=False)
    slug = models.SlugField(blank=True, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    tagline = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.name

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
    blog = models.ForeignKey(Blog)
    title = models.CharField(blank=False, max_length=100,
            verbose_name="Post Title")
    slug = models.SlugField(blank=False, unique_for_date='posted')
    body = models.TextField(blank=False, verbose_name="Post Contents")
    # change to user profile
    author = models.CharField(blank=False, max_length=30)
    edited = models.DateTimeField(blank=True,
            default=datetime.datetime.now, verbose_name="Last Edited",
            editable=False)
    posted = models.DateTimeField(blank=True, default=datetime.datetime.now,
            verbose_name="Publication Date")
    status = models.CharField(blank=False, max_length=2,
            choices=PUBLICATION_LEVEL, default="DR")
    sticky = models.BooleanField(default=False)
    visibility = models.CharField(blank=False, max_length=2,
            choices=VISIBILITY_LEVEL, default="VI")
    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def save(self):
        self.edited = datetime.datetime.now
        super(Entry, self).save()

    def perma_link(self):
        kwargs = {
            "year": self.posted.year,
            "month": "%02d" % self.posted.month,
            "day": "%02d" % self.posted.day,
            "slug": self.slug,
        }
        if self.blog.slug:
            kwargs["blog"] = self.blog.slug
        return reverse("blog-post", kwargs=kwargs)

class EntryMenuLink(MenuLink):
    entry = models.ForeignKey(Entry, null=False, blank=False)

    def get_location(self):
        return self.entry.perma_link()