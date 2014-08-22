from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.core.models import Property
from django.core.urlresolvers import reverse

class ForumGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    tagline = models.TextField(blank=True, null=False)
    sites = models.ManyToManyField(Site, related_name="forums")

    #options
    format = models.CharField(max_length=20)

    properties = models.ManyToManyField(Property, blank=True, null=True)
    
    def __str__(self):
        return str(self.name)
    
    def save(self):
        if self.slug == "":
            self.slug = None
        super(ForumGroup, self).save()

    def get_absolute_url(self):
        if self.slug:
            return reverse("forum-index", kwargs={"forums": self.slug})
        return reverse("forum-index")
    

class ForumCategory(models.Model):
    """
    Describes the categories that each forum is grouped with in.
    """
    name = models.CharField(max_length=100, unique=True)
    position = models.IntegerField(default=1)
    forums = models.ForeignKey(ForumGroup, related_name="category")
    
    def __str__(self):
        return str(self.name)

class Forum(models.Model):
    """
    The Forums which threads can be put in.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    #redirect_url
    topics = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    last_post = models.ForeignKey('Post', null=True, blank=True)
    position = models.IntegerField(default=1)
    category = models.ForeignKey('ForumCategory', null=True, blank=True, related_name="forum")
    parent_forum = models.ForeignKey('self', null=True, blank=True, related_name="children")
    password = models.CharField(max_length=50, null=True, blank=True)

    subscriptions = models.OneToOneField(User, null=True, blank=True, related_name='forum_forum_subscriptions')

    def __str__(self):
        return str(self.name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('djangopress.forum.views.view_forum', [str(self.id)])

class Post(models.Model):
    author = models.ForeignKey(User, related_name="forum_posts", blank=True,  null=True)

    ## for anonymous users
    poster_name = models.CharField(blank=True, null=True, max_length=50)
    poster_email = models.EmailField(blank=True, null=True)

    ip = models.IPAddressField()
    message = models.TextField()
    thread = models.ForeignKey('Thread', related_name="posts")
    
    # we record this here is even if the format of the forum changes
    # old posts will still render in the format they are written in
    format = models.CharField(max_length=20)

    show_similies = models.BooleanField(default=True, help_text="Show icons as smilies for this post.")

    posted = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, related_name="forum_posts_edited", blank=True, null=True)
    edited = models.DateTimeField(null=True, blank=True)
    edit_reason = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return "%s %s" % (self.thread.subject, self.posted)


class Thread(models.Model):
    class Meta:
        #need to move around
        permissions = (
            ('can_read_forum', 'User is allowed to read forum'),
            ('can_post_replies', 'User is allowed to reply to threads'),
            ('can_post_threads', 'User is allowed to post new thread')
        )
    ## for anonymous users
    poster_name = models.CharField(blank=True, null=True, max_length=50)
    poster_email = models.EmailField(blank=True, null=True)
    
    subscriptions = models.ManyToManyField(User, related_name='forum_subscriptions')

    poster = models.ForeignKey(User, blank=True, null=True)
    subject = models.CharField(max_length=255)
    posted = models.DateTimeField(auto_now_add=True)
    
    first_post = models.ForeignKey(Post, blank=True, null=True, related_name='thread_first')
    last_post = models.ForeignKey(Post, blank=True, null=True, related_name='thread_last')
    num_views = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    moved_to = models.ForeignKey('Thread', blank=True, null=True)
    forum = models.ForeignKey(Forum)
    
    def __str__(self):
        return str(self.subject)

class Rank(models.Model):
    """
    The titles the user gets as they make more posts
    """
    name = models.CharField(max_length=50)
    min_posts = models.IntegerField()

class Report(models.Model):
    """
    The reported posts for spamming etc
    """
    post = models.ForeignKey(Post, related_name="reports")
    thread = models.ForeignKey(Thread, related_name="reports")
    forum = models.ForeignKey(Forum, related_name="reports")
    reported_by = models.ForeignKey(User, related_name="forum_reports")
    created_date = models.DateTimeField(auto_now_add=True)
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
    
    sig = models.TextField(default="")

    email_settings = models.CharField(choices=EMAIL_SETTINGS, default='HI', max_length=2)
    notify = models.CharField(choices=NOFITY, default='AL', max_length=2)

    show_simlies = models.BooleanField(default=True)
    show_img = models.BooleanField(default=True)
    show_avatars = models.BooleanField(default=True)
    show_sig = models.BooleanField(default=True)

class Attachment(models.Model):
    post = models.ForeignKey('Post', related_name="attachments")
    thread = models.ForeignKey('Thread', related_name="attachments")

    poster = models.ForeignKey(User, related_name="forum_attachments")
    download_count = models.IntegerField(default=0)
    comment = models.TextField()
    attachment = models.FileField(upload_to='forum/upload/%Y/%m/%d/')

    #extension
    #mimetype
    #filesize
    #filetime
    #thumbnail = FilePathField
    #location_file_name
    #display_file_name
