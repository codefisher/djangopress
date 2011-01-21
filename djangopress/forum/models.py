from django.db import models

# Create your models here.

class ForumCategories(models.Model):
    """
    Describes the categories that each forum is grouped with in.
    """
    #name
    #position

class Forum(models.Model):
    """
    The Forums which threads can be put in.
    """
    #name
    #description
    #redirect_url
    #topics
    #posts
    #last post
    #position
    #category
    #parent forum
    #password (to limit access)


class Post(models.Model):
    pass
    #user

    ## for anonimouse users
    #poster_id
    #poster_email

    #ip
    #message
    #thread
    #options (show_similies, use bbcode, show sig)

    #posted
    #edited_by
    #edited
    #edit reason
    #attachments

class Thread(models.Model):
    class Meta:
        #need to move around
        permissions = (
            ('can_read_forum', 'User is allowed to read forum'),
            ('can_post_replies', 'User is allowed to reply to threads'),
            ('can_post_threads', 'User is allowed to post new thread')
        )
    pass
    #poster
    #subject
    #posted
    #last post
    #num views
    #num posts
    #closed
    #sticky
    #moved_to (another forum?)
    #forum

class Rank(models.Model):
    """
    The titles the user gets as they make more posts
    """
    #name
    #min_posts

class Reports(models.Model):
    """
    The reported posts for spamming etc
    """
    #post
    #thread
    #forum
    #reported_by
    #created date
    #message
    #moderated
    #moderated_by


class Subscriptions(models.Model):
    """
    Email subscriptions to threads
    """
    #user
    #topic

class ForumSubscriptions(models.Model):
    """
    Email subscriptions to forums
    """
    #user
    #forum

class ForumUser(models.Model):
    """
    User class for forum
    """
    #num_topics
    #num_posts

    #email settings
    #notify
    #show smilies, img, img_sig, avatars, sig

class Attachment(models.Model):
    """
    post
    topic
    poster
    location_file_name
    displya_file_name
    download_count
    comment
    extension
    mimetype
    filesize
    filetime
    thumbnail
    """

class BBcode(models.Model):
    pass


class ForumConfig(models.Model):
    pass
    #name
    #value