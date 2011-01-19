import datetime
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.TextField(blank=True, null=False)
    slug = models.SlugField(blank=True, unique=True)

class Category(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.TextField(blank=True, null=False)
    slug = models.SlugField(blank=True, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True)

class Blog(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    slug = models.SlugField(blank=True, unique=True)
    tagline = models.TextField(blank=True, null=False)

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
    blog = models.ForeignKey(Blog, null=True)
    title = models.CharField(blank=False, max_length=100,
            verbose_name="Post Title")
    slug = models.SlugField(blank=True, unique=True)
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
    tags = models.ManyToManyField(Tag)
    categories = models.ManyToManyField(Category)