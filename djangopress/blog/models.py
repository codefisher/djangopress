import datetime
import time

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.core.util import smart_truncate_chars
from django.utils.safestring import mark_safe
from djangopress.core.format.html import extended_html
import markdown
import bleach

class EntryMananger(models.Manager):

    def get_entries(self, blog=None, ordered=True):
        entry_list = self.select_related('blog', 'author').prefetch_related(
                models.Prefetch('tags', queryset=Tag.objects.select_related('blog')), 
                models.Prefetch('categories', queryset=Category.objects.select_related('blog'))).filter(status="PB", visibility="VI")
        if blog is not None:
            entry_list = entry_list.filter(blog=blog)
        if ordered:
            return entry_list.order_by('-sticky', '-posted')
        return entry_list
    
class CategoryMananger(models.Manager):

    def get_categories(self, blog=None, ordered=True):
        categories_list = self.select_related('blog', 'parent_category').all()
        if blog is not None:
            categories_list = categories_list.filter(blog=blog)
        if ordered:
            return categories_list.order_by('name')
        return categories_list

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
    
    def get_feed_url(self):
        return reverse("blog-feed", kwargs={"blog_slug": self.slug})
    
def post_image_path(instance, filename):
    if instance.pk:
        return ("blog/%s/%s-%s" % (time.strftime("%y/%m"), instance.pk, filename.lower()))
    return ("blog/%s/%s" % (time.strftime("%y/%m"), filename.lower()))

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
    edited_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name="blog_edited_entries")
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
    
    # meta data
    description = models.TextField(blank=True, max_length=140, default="")
    post_image = models.ImageField(blank=True, null=True, upload_to=post_image_path)

    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"

    objects = EntryMananger()

    def __unicode__(self):
        return self.title

    def save(self):
        super(Entry, self).save()
        
    def get_description(self):
        if self.description:
            return self.description
        return smart_truncate_chars(bleach.clean(self.body, strip=True, tags=()).strip(), 140)
        
    def get_tags(self):
        return self.tags.all()
    
    def get_categories(self):
        return self.categories.all()

    def format_body(self):
        return extended_html(self.body)

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
    
    def formatted_comment(self):
        return mark_safe(markdown.markdown(bleach.clean(self.comment_text, strip=True)))
    
    def get_user_name(self):
        return self.user.username if self.user else self.user_name
    
    def get_user_url(self):
        return self.user.profile.homepage if self.user and self.user.profile else self.user_url

class Flag(models.Model):
    user = models.ForeignKey(User, related_name="comment_flags")
    comment = models.ForeignKey(Comment, related_name="flag")
    flag = models.CharField('flag', max_length=100)
    flag_date = models.DateTimeField(auto_now_add=True)
