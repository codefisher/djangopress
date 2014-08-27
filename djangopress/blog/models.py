import datetime
from django.db import models
from django.core.urlresolvers import reverse
from djangopress.core.links.models import Link
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.blog.managers import EntryMananger, CategoryMananger

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
        return reverse("blog-tag", kwargs={"slug": self.slug, "blog_slug": self.blog.slug})

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True,
            related_name="child_categories")
    blog = models.ForeignKey("Blog", related_name="categories")
    
    objects = CategoryMananger()

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        unique_together = ("slug", "blog")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog-category", kwargs={"slug": self.slug, "blog_slug": self.blog.slug})

class Blog(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    tagline = models.TextField(blank=True, null=False)
    sites = models.ManyToManyField(Site)

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __unicode__(self):
        return self.name
    
    def save(self):
        if self.slug == "":
            self.slug = None
        super(Blog, self).save()

    def get_absolute_url(self, page=None):
        if page is None:
            return reverse("blog-index", kwargs={"blog_slug": self.slug})
        return reverse("blog-index", kwargs={"blog_slug": self.slug, "page": page})

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
    comments_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"

    objects = EntryMananger()

    def __unicode__(self):
        return self.title

    def save(self):
        super(Entry, self).save()
        
    def get_tags(self):
        return self.tags.all().select_related('blog')
    
    def get_categories(self):
        return self.categories.all().select_related('blog')

    def get_absolute_url(self):
        kwargs = {
            "year": self.posted.year,
            "month": "%02d" % self.posted.month,
            "day": "%02d" % self.posted.day,
            "slug": self.slug,
            "blog_slug": self.blog.slug,
        }
        return reverse("blog-post", kwargs=kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name="blog_comments")
    user_name = models.CharField(verbose_name="Name", max_length=50, blank=True)
    user_email = models.EmailField(verbose_name="Email address", blank=True)
    user_url = models.URLField(verbose_name="Website", blank=True)
   
    comment_text = models.TextField(max_length=5000)
    entry = models.ForeignKey(Entry)
    parent = models.ForeignKey("Comment", null=True, blank=True)
    rank = models.IntegerField(default=0)
    
    # Metadata about the comment
    submit_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField('IP address', blank=True, null=True)
    user_agent = models.TextField(blank=True)
    is_public = models.BooleanField('is public', default=True,
        help_text='Uncheck this box to make the comment effectively ' \
                'disappear from the site.')
    is_removed = models.BooleanField('is removed', default=False,
        help_text='Check this box if the comment is inappropriate. ' \
                'A "This comment has been removed" message will ' \
                'be displayed instead.')
    is_spam = models.BooleanField('is spam', default=False,
        help_text='Check this box to flag as spam.')

class Flag(models.Model):
    user = models.ForeignKey(User, related_name="comment_flags")
    comment = models.ForeignKey(Comment, related_name="flag")
    flag = models.CharField('flag', max_length=100)
    flag_date = models.DateTimeField(auto_now_add=True)