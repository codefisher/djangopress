import datetime
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.core.models import Property

# Create your models here.

class Forums(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    tagline = models.TextField(blank=True, null=False)
    sites = models.ManyToManyField(Site, related_name="forums")

    #options
    format = models.CharField(max_length=20)

    properties = models.ManyToManyField(Property, blank=True, null=True)

class ForumCategories(models.Model):
    """
    Describes the categories that each forum is grouped with in.
    """
    name = models.CharField(max_length=100, unique=True)
    position = models.IntegerField(default=1)
    forums = models.ForeignKey(Forums, related_name="category")

class Forum(models.Model):
    """
    The Forums which threads can be put in.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    #redirect_url
    topics = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    last_post = models.ForeignKey('Post')
    position = models.IntegerField(default=1)
    parent_forum = models.ForeignKey('self', null=True, related_name="children")
    password = models.CharField(max_length=50, null=True, blank=True)

    subscriptions = models.OneToOneField(User, related_name='forum_forum_subscriptions')


class Post(models.Model):
    author = models.ForeignKey(User, related_name="forum_posts", blank=True,  null=True)

    ## for anonymous users
    poster_name = models.CharField(blank=True, max_length=50)
    poster_email = models.EmailField(blank=True)

    ip = models.IPAddressField()
    message = models.TextField()
    thread = models.ForeignKey('Thread', relatedName="posts")
    format = models.CharField(max_length=20)

    show_similies = models.BooleanField(default=True)

    posted = models.DateField(default=datetime.datetime.now)
    edited_by = models.ForeignKey(User, related_name="forum_posts_edited", blank=True, null=True)
    edited = models.DateField(null=True, blank=True)
    edit_reason = models.TextField(null=True, blank=True)


class Thread(models.Model):
    class Meta:
        #need to move around
        permissions = (
            ('can_read_forum', 'User is allowed to read forum'),
            ('can_post_replies', 'User is allowed to reply to threads'),
            ('can_post_threads', 'User is allowed to post new thread')
        )

    subscriptions = models.OneToOneField(User, related_name='forum_subscriptions')

    poster = models.ForeignKey(User, blank=True, null=True)
    subject = models.CharField(max_length=255)
    posted = models.DateField(default=datetime.datetime.now)
    first_post = models.ForeignKey(Post, blank=True)
    last_post = models.ForeignKey(Post, blank=True)
    num_views = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    moved_to = models.ForeignKey('Thread', blank=True)
    forum = models.ForeignKey(Forum)

class Rank(models.Model):
    """
    The titles the user gets as they make more posts
    """
    name = models.CharField()
    min_posts = models.IntegerField()

class Reports(models.Model):
    """
    The reported posts for spamming etc
    """
    post = models.ForeignKey(Post, related_name="reports")
    thread = models.ForeignKey(Thread, related_name="reports")
    forum = models.ForeignKey(Forum, related_name="reports")
    reported_by = models.ForeignKey(User, related_name="forum_reports")
    created_date = models.DateField(default=datetime.datetime.now)
    message = models.TextField()
    moderated = models.BooleanField(default=False)
    moderated_by = models.ForeignKey(User, related_name="forum_moderated_reports")


class ForumUser(models.Model):
    """
    User class for forum
    """

    EMAIL_SETTINGS = (
        ('HI', 'Hide Email'),
        ('SW', 'Show Email'),
        ('HB', 'Hide email but allow people to contact me though them forum')
    )

    NOFITY = (
       ('AL', 'Always Notify'),
       ('NV', 'Never Notify'),
       ('DN', 'Send daily digest')
    )

    user = models.OneToOneField(User, related_name='forum_profile')
    num_topics = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)

    email_settings = models.CharField(choices=EMAIL_SETTINGS, default='HI')
    notify = models.CharField()

    show_simlies = models.BooleanField(default=True)
    img = models.BooleanField(default=True)
    avatars = models.BooleanField(default=True)
    sig = models.BooleanField(default=True)

class Attachment(models.Model):
    post = models.ForeignKey('Post', related_name="attachments")
    thread = models.ForeignKey('Thread', related_name="attachments")

    poster = models.ForeignKey(User, related_name="forum_attachments")
    #location_file_name
    #display_file_name
    #download_count
    #comment
    #extension
    #mimetype
    #filesize
    #filetime
    #thumbnail = FilePathField
