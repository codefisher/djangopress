from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from djangopress.core.models import Property
from django.core.urlresolvers import reverse
from djangopress.core.format import Library
from djangopress.core import format

class ForumGroup(models.Model):
    
    class Meta:
        permissions = (
            ('can_read_forum_group', 'User is allowed to read forum'), #not impl
        )
        
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    tagline = models.TextField(blank=True, null=False)
    sites = models.ManyToManyField(Site, related_name="forums")

    #options
    format = models.CharField(max_length=20, choices=format.Library.choices(False))
    show_announcement = models.BooleanField(default=False)
    announcement = models.TextField(blank=True, null=True)
    number_of_threads = models.IntegerField(default=40)
    number_of_posts = models.IntegerField(default=20)
    show_smilies = models.BooleanField(default=True)
    display_images = models.BooleanField(default=True)
    make_links = models.BooleanField(default=True)
    show_avatars = models.BooleanField(default=True)
    show_signature = models.BooleanField(default=True) 
    show_quick_post = models.BooleanField(default=True)
    post_redirect_delay = models.IntegerField(default=3, help_text="How long to show the successful post page, before redirecting.  Set to 0 to disable.")
    
    def __unicode__(self):
        return self.name

    def get_format(self):
        return Library.get(self.format)
    
    def save(self):
        if self.slug == "":
            self.slug = None
        super(ForumGroup, self).save()

    def get_absolute_url(self):
        return reverse("forum-index", kwargs={"forums_slug": self.slug})
    
class ForumProperty(Property):
    forums = models.ForeignKey(ForumGroup, related_name="properties")

class ForumCategory(models.Model):
    """
    Describes the categories that each forum is grouped with in.
    """
    name = models.CharField(max_length=100, unique=True)
    position = models.IntegerField(default=1)
    forums = models.ForeignKey(ForumGroup, related_name="category")
    
    def __unicode__(self):
        return self.name
    
    def get_forums(self):
        return self.forum.all().order_by('position')

    def get_absolute_url(self):
        return reverse("forum-category", kwargs={"forums_slug": self.forums.slug, "category_id":self.pk })

class ForumMananger(models.Manager):

    def items(self):
        return super(ForumMananger, self).all().order_by('position').defer('last_post__message').select_related('last_post', 'last_post__author', 'last_post__thread__forum__category__forums')

class Forum(models.Model):
    """
    The Forums which threads can be put in.
    """
    class Meta:
        permissions = (
            ('can_post_threads', 'User is allowed to post new thread'),
            ('can_close_threads', 'User is allowed to close a thread'), #not impl
            ('can_sticky_threads', 'User is allowed to sticky a thread'), #not impl
            ('can_moderate_forum', 'Has access to all the batch moderation options'), #not impl ? should we ?
        )
        
    objects = ForumMananger()
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    #redirect_url
    num_threads = models.IntegerField(default=0, verbose_name='Number of Threads')
    num_posts = models.IntegerField(default=0, verbose_name='Number of Posts')
    last_post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.IntegerField(default=1)
    category = models.ForeignKey('ForumCategory', null=True, blank=True, related_name="forum")
    parent_forum = models.ForeignKey('self', null=True, blank=True, related_name="children")
    password = models.CharField(max_length=50, null=True, blank=True)

    subscriptions = models.ManyToManyField(User, null=True, blank=True, related_name='forum_forum_subscriptions')

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self, page=None):
        if page is None or page == 1:
            return reverse("forum-view", kwargs={"forums_slug": self.category.forums.slug, 'forum_id': self.id})  
        return reverse("forum-view", kwargs={"forums_slug": self.category.forums.slug, 'forum_id': self.id, 'page': page})  

class Post(models.Model):
    
    class Meta:
        permissions = (
            ('can_edit_own_posts', 'User is allowed to edit posts they have made'),
            ('can_edit_others_posts', 'User is allowed to edit posts others have made'),
            ('can_mark_removed', 'Can mark the post as removed/not removed'),
            ('can_mark_public', 'Can mark if a post is public or not'),
            ('can_mark_spam', 'Can mark a post as spam/not spam')
        )
        
    author = models.ForeignKey(User, related_name="forum_posts", blank=True,  null=True)

    ## for anonymous users
    poster_name = models.CharField(blank=True, null=True, max_length=50)
    poster_email = models.EmailField(blank=True, null=True)

    ip = models.GenericIPAddressField()
    message = models.TextField()
    thread = models.ForeignKey('Thread', related_name="posts")
    
    # we record this here is even if the format of the forum changes
    # old posts will still render in the format they are written in
    format = models.CharField(max_length=20)

    show_similies = models.BooleanField(default=True, help_text="Show smilies as icons for this post.")

    posted = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, related_name="forum_posts_edited", blank=True, null=True)
    edited = models.DateTimeField(null=True, blank=True)
    edit_reason = models.CharField(null=True, blank=True, max_length=200)
    
    is_public = models.BooleanField('is public', default=True,
        help_text='Uncheck this box to make the post effectively ' \
                'disappear from the site.')
    is_removed = models.BooleanField('is removed', default=False,
        help_text='Check this box if the post is inappropriate. ' \
                'A "This post has been removed" message will ' \
                'be displayed instead.')
    is_spam = models.BooleanField('is spam', default=False,
        help_text='Check this box to flag as spam.')
    
    def get_format(self):
        return Library.get(self.format)
    
    def __unicode__(self):
        return u"%s %s" % (self.thread.subject, self.posted)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.__original_is_public = self.is_public
        self.__original_is_spam = self.is_spam
   
    def __changed_status_visiable(self):
        return ((not self.__original_is_public and self.is_public and not self.is_spam)
                or (self.__original_is_spam and not self.is_spam and self.is_public))
    def __change_status_invisible(self):
        return ((self.__original_is_public and not self.is_public) or (not self.__original_is_spam and self.is_spam))
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Post, self).save(*args, **kwargs)
        if (is_new and self.is_public and not self.is_spam) or (not is_new and self.__changed_status_visiable()):
            first_post = self.thread.first_post
            if is_new and self.thread.first_post_id == None:
                first_post = self
            if is_new:
                last_post = self
            else:
                last_post = Post.objects.filter(thread=self.thread, is_spam=False, is_public=True).order_by('-posted')[0]
            Thread.objects.filter(pk=self.thread.pk).update(num_posts=models.F('num_posts') + 1, first_post=first_post, last_post_date=last_post.posted, last_post=last_post)
            Forum.objects.filter(pk=self.thread.forum.pk).update(num_posts=models.F('num_posts') + 1, last_post=last_post)
            if self.author:
                ForumUser.objects.get_or_create(user=self.author)
                ForumUser.objects.filter(user=self.author).update(num_posts=models.F('num_posts') + 1)
        elif (not is_new and self.__change_status_invisible()):
            self._decriment_posts()
        self.__original_is_public = self.is_public
        self.__original_is_spam = self.is_spam
        
    def delete(self, *args, **kwargs):
        if self.is_public and not self.is_spam:
            self._decriment_posts()
        super(Post, self).delete(*args, **kwargs)
        posts = Post.objects.filter(thread=self.thread).exclude(pk=self.pk)
        if not posts:
            # there are no posts left at all
            self.thread.delete()
            
    def _decriment_posts(self):
        if self.thread_id and self.thread.last_post_id:
            last_post = self.thread.last_post
        else:
            last_post = None
        if self.thread.last_post_id is None or self.thread.last_post == self:
            try:
                last_post = Post.objects.filter(thread=self.thread, is_spam=False, is_public=True).exclude(pk=self.pk).order_by('-posted')[0]
            except:
                self.thread.last_post = None
        forum = Forum.objects.filter(pk=self.thread.forum.pk)
        if self.thread.forum.last_post_id == None or self.thread.forum.last_post == self:
            forum.update(last_post=Post.objects.filter(thread__forum=self.thread.forum, is_spam=False, is_public=True).exclude(pk=self.pk).order_by('-posted')[0])
        if self.thread and self.thread.first_post_id == None:
            first_post = self.thread.first_post
        else:
            first_post = None
        if self.thread.first_post_id == None or self.thread.first_post == self:
            try:
                first_post = Post.objects.filter(thread=self.thread, is_spam=False, is_public=True).exclude(pk=self.pk).order_by('posted')[0]
            except:
                first_post = None
        Thread.objects.filter(pk=self.thread.pk).update(num_posts=models.F('num_posts') - 1, first_post=first_post, last_post_date=last_post.posted if last_post else None, last_post=last_post)
        forum.update(num_posts=models.F('num_posts') - 1)
        if self.author:
            ForumUser.objects.filter(user=self.author).update(num_posts=models.F('num_posts') - 1)

    def author_name(self):
        if self.author is None:
            return self.poster_name
        return self.author.username
    
    def get_page(self):
        return Post.objects.filter(thread=self.thread, posted__lt=self.posted, is_spam=False, is_public=True).order_by('posted').count()/(self.thread.forum.category.forums.number_of_posts) + 1
    
    def get_absolute_url(self):
        return reverse('forum-view-post', kwargs={"forums_slug": self.thread.forum.category.forums.slug, 'post_id': self.pk})
    
           
class Thread(models.Model):
    class Meta:
        permissions = (
            ('can_post_replies', 'User is allowed to reply to threads'),
        )
    ## for anonymous users
    poster_name = models.CharField(blank=True, null=True, max_length=50)
    poster_email = models.EmailField(blank=True, null=True)
    
    subscriptions = models.ManyToManyField(User, null=True, blank=True, related_name='forum_subscriptions')

    poster = models.ForeignKey(User, blank=True, null=True)
    subject = models.CharField(max_length=255)
    posted = models.DateTimeField(auto_now_add=True)
    
    first_post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True, related_name='thread_first')
    last_post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True, related_name='thread_last')
    last_post_date = models.DateTimeField(null=True, blank=True)
    
    num_views = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    moved_to = models.ForeignKey('Thread', blank=True, null=True) # not implimented
    forum = models.ForeignKey(Forum)
    
    def __unicode__(self):
        return self.subject
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Thread, self).save(*args, **kwargs)
        if is_new:
            Forum.objects.filter(pk=self.forum.pk).update(num_threads=models.F('num_threads') + 1)
            if self.poster:
                ForumUser.objects.get_or_create(user=self.poster)
                ForumUser.objects.filter(user=self.poster).update(num_threads=models.F('num_threads') + 1)
                
    def delete(self, *args, **kwargs):
        super(Thread, self).delete(*args, **kwargs)
        Forum.objects.filter(pk=self.forum.pk).update(num_threads=models.F('num_threads') - 1)
        if self.poster:
            ForumUser.objects.filter(user=self.poster).update(num_threads=models.F('num_threads') - 1)
                
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
    # we have not implement this, how it is to work with a site wide
    # user system
    name = models.CharField(max_length=50)
    min_posts = models.IntegerField()

class Report(models.Model):
    """
    The reported posts for spamming etc
    """
    post = models.ForeignKey(Post, related_name="reports")
    reported_by = models.ForeignKey(User, null=True, blank=True, related_name="forum_reports")
    created_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    moderated = models.BooleanField(default=False)
    moderated_by = models.ForeignKey(User, blank=True, null=True, related_name="forum_moderated_reports")
    
    def __unicode__(self):
        return u"Report for %s" % unicode(self.post)

class ForumUser(models.Model):
    """
    User class for forum
    """

    NOFITY = (
       ('AL', 'Always Notify'),
       ('NV', 'Never Notify'),
       #('DN', 'Send daily digest')
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
    #thread = models.ForeignKey('Thread', related_name="attachments")

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
