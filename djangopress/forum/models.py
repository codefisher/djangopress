from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.core.models import Property
from django.core.urlresolvers import reverse
from djangopress.core.format import Library

THREADS_PER_PAGE = 40
POSTS_PER_PAGE = 10

class ForumGroup(models.Model):
    
    class Meta:
        permissions = (
            ('can_read_forum_group', 'User is allowed to read forum'),
        )
        
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
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
        return reverse("forum-index", kwargs={"forums_slug": self.slug})  

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
    class Meta:
        permissions = (
            ('can_post_threads', 'User is allowed to post new thread'),
            ('can_close_threads', 'User is allowed to close a thread'),
            ('can_sticky_threads', 'User is allowed to sticky a thread'),
        )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    #redirect_url
    num_threads = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    last_post = models.ForeignKey('Post', null=True, blank=True)
    position = models.IntegerField(default=1)
    category = models.ForeignKey('ForumCategory', null=True, blank=True, related_name="forum")
    parent_forum = models.ForeignKey('self', null=True, blank=True, related_name="children")
    password = models.CharField(max_length=50, null=True, blank=True)

    subscriptions = models.ManyToManyField(User, null=True, blank=True, related_name='forum_forum_subscriptions')

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self, page=None):
        if page is None or page == 1:
            return reverse("forum-view", kwargs={"forums_slug": self.category.forums.slug, 'forum_id': self.id})  
        return reverse("forum-view", kwargs={"forums_slug": self.category.forums.slug, 'forum_id': self.id, 'page': page})  

class Post(models.Model):
    
    class Meta:
        permissions = (
            ('can_edit_owns_posts', 'User is allowed to edit posts they have made'),
            ('can_edit_others_posts', 'User is allowed to edit posts others have made'),
        )
        
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

    posted = models.DateTimeField()#auto_now_add=True)
    edited_by = models.ForeignKey(User, related_name="forum_posts_edited", blank=True, null=True)
    edited = models.DateTimeField(null=True, blank=True)
    edit_reason = models.TextField(null=True, blank=True)
    
    is_public = models.BooleanField('is public', default=True,
        help_text='Uncheck this box to make the post effectively ' \
                'disappear from the site.')
    is_removed = models.BooleanField('is removed', default=False,
        help_text='Check this box if the post is inappropriate. ' \
                'A "This post has been removed" message will ' \
                'be displayed instead.')
    is_spam = models.BooleanField('is spam', default=False,
        help_text='Check this box to flag as spam.')
    
    def __str__(self):
        return "%s %s" % (self.thread.subject, self.posted)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.__original_is_public = self.is_public
        self.__original_is_spam = self.is_spam
    
    def formatted(self):
        formating = Library.get(self.format).get("function")
        return formating(self.message)
    
    def __changed_status_visiable(self):
        return ((not self.__original_is_public and self.is_public and not self.is_spam)
                or (self._original_is_spam and not self.is_span and self.is_public))
    def __change_status_invisible(self):
        return ((self.__original_is_public and not self.is_public) or (not self.__original_is_span and self.is_spam))
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Post, self).save(*args, **kwargs)
        if (is_new and self.is_public and not self.is_spam) or (not is_new and self.__changed_status_visiable()):
            if is_new and self.thread.first_post is None:
                self.thread.first_post = self
            if is_new:
                self.thread.last_post = self
            else:
                self.thread.last_post = Post.objects.filter(thread=self.thread, is_spam=False, is_public=True).order_by('posted')[-1]
                self.thread.last_post_date = self.thread.last_post.posted
            self.thread.forum.last_post = self.thread.last_post
            self.thread.num_posts += 1
            self.thread.save()
            self.thread.forum.num_posts += 1
            self.thread.forum.save()
            if self.author:
                profile = ForumUser.objects.get_or_create(user=self.author)[0]
                profile.num_posts += 1
                profile.save()
        elif (not is_new and self.__change_status_invisible()):
            self._decriment_posts()
        self.__original_is_public = self.is_public
        self.__original_is_spam = self.is_spam
        
    def delete(self, *args, **kwargs):
        super(Post, self).delete(*args, **kwargs)
        self._decriment_posts()
            
    def _decriment_posts(self):
        if self.thread.last_post.pk == self.pk:
            self.thread.last_post = Post.objects.filter(thread=self.thread, is_spam=False, is_public=True).order_by('posted')[-1]
            self.thread.last_post_date = self.thread.last_post.posted
            self.thread.forum.last_post = self.thread.last_post
            self.thread.forum.save()
        self.thread.num_posts -= 1
        self.thread.save()
        self.thread.forum.num_posts -= 1
        self.thread.forum.save()
        if self.author:
            profile = ForumUser.objects.get_or_create(user=self.author)[0]
            profile.num_posts -= 1
            profile.save()
            
    def author_name(self):
        if self.author is None:
            return self.poster_name
        return self.author.username
    
    def get_page(self):
        return Post.objects.filter(thread=self.thread, posted__lt=self.posted).order_by('posted').count()/POSTS_PER_PAGE +1
    
    def get_absolute_url(self):
        return reverse('forum-view-post', kwargs={"forums_slug": self.thread.forum.category.forums.slug, 'post_id': self.id})
    
class Thread(models.Model):
    class Meta:
        permissions = (
            ('can_post_replies', 'User is allowed to reply to threads'),
        )
    ## for anonymous users
    poster_name = models.CharField(blank=True, null=True, max_length=50)
    poster_email = models.EmailField(blank=True, null=True)
    
    subscriptions = models.ManyToManyField(User, related_name='forum_subscriptions')

    poster = models.ForeignKey(User, blank=True, null=True)
    subject = models.CharField(max_length=255)
    posted = models.DateTimeField()#auto_now_add=True)
    
    first_post = models.ForeignKey(Post, blank=True, null=True, related_name='thread_first')
    last_post = models.ForeignKey(Post, blank=True, null=True, related_name='thread_last')
    last_post_date = models.DateTimeField(null=True, blank=True)
    
    num_views = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    moved_to = models.ForeignKey('Thread', blank=True, null=True)
    forum = models.ForeignKey(Forum)
    
    def __str__(self):
        return str(self.subject)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Thread, self).save(*args, **kwargs)
        if is_new:
            self.forum.num_threads += 1
            self.forum.save()
            if self.poster:
                profile = ForumUser.objects.get_or_create(user=self.poster)[0]
                profile.num_threads += 1
                profile.save()
                
    def delete(self, *args, **kwargs):
        super(Thread, self).delete(*args, **kwargs)
        self.forum.num_threads -= 1
        self.forum.save()
        if self.poster:
            profile = ForumUser.objects.get_or_create(user=self.poster)[0]
            profile.num_threads -= 1
            profile.save()
                
    def get_absolute_url(self, page=None):
        if page is None or page == 1:
            return reverse("forum-view-thread", kwargs={"forums_slug": self.forum.category.forums.slug, 'thread_id': self.id})
        return reverse("forum-view-thread", kwargs={"forums_slug": self.forum.category.forums.slug, 'thread_id': self.id, 'page': page})

    def author_name(self):
        if self.poster is None:
            return self.poster_name
        return self.poster.username
    
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
    reported_by = models.ForeignKey(User, related_name="forum_reports")
    created_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    moderated = models.BooleanField(default=False)
    moderated_by = models.ForeignKey(User, related_name="forum_moderated_reports")


class ForumUser(models.Model):
    """
    User class for forum
    """

    NOFITY = (
       ('AL', 'Always Notify'),
       ('NV', 'Never Notify'),
       ('DN', 'Send daily digest')
    )

    user = models.OneToOneField(User, related_name='forum_profile')
    num_threads = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    
    #sig = models.TextField(default="")

    notify = models.CharField(choices=NOFITY, default='AL', max_length=2)

    show_simlies = models.BooleanField(default=True, help_text="Show smilies in forum posts.")
    show_img = models.BooleanField(default=True, verbose_name="Show Images", help_text="Show images in forum posts.")
    show_avatars = models.BooleanField(default=True, help_text="Show that avatar images of users.")
    show_sig = models.BooleanField(default=True, verbose_name="Show Signature", help_text="Show user signature after their posts.")

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
