# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class PunAkismet(models.Model):
    id = models.IntegerField(primary_key=True)
    poster = models.CharField(max_length=600)
    poster_id = models.IntegerField()
    poster_ip = models.CharField(max_length=45, blank=True)
    poster_email = models.CharField(max_length=150, blank=True)
    subject = models.CharField(max_length=765)
    message = models.TextField()
    hide_smilies = models.IntegerField()
    posted = models.IntegerField()
    edited = models.IntegerField(null=True, blank=True)
    edited_by = models.CharField(max_length=600, blank=True)
    topic_id = models.IntegerField()
    forum_id = models.IntegerField()
    class Meta:
        db_table = u'pun_akismet'

class PunBans(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=600, blank=True)
    ip = models.CharField(max_length=765, blank=True)
    email = models.CharField(max_length=150, blank=True)
    message = models.CharField(max_length=765, blank=True)
    expire = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'pun_bans'

class PunCategories(models.Model):
    id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=240)
    disp_position = models.IntegerField()
    class Meta:
        db_table = u'pun_categories'

class PunCensoring(models.Model):
    id = models.IntegerField(primary_key=True)
    search_for = models.CharField(max_length=180)
    replace_with = models.CharField(max_length=180)
    class Meta:
        db_table = u'pun_censoring'

class PunConfig(models.Model):
    conf_name = models.CharField(max_length=765, primary_key=True)
    conf_value = models.TextField(blank=True)
    class Meta:
        db_table = u'pun_config'

class PunForumPerms(models.Model):
    group_id = models.IntegerField(primary_key=True)
    forum_id = models.IntegerField(primary_key=True)
    read_forum = models.IntegerField()
    post_replies = models.IntegerField()
    post_topics = models.IntegerField()
    class Meta:
        db_table = u'pun_forum_perms'

class PunForums(models.Model):
    id = models.IntegerField(primary_key=True)
    forum_name = models.CharField(max_length=240)
    forum_desc = models.TextField(blank=True)
    redirect_url = models.CharField(max_length=300, blank=True)
    moderators = models.TextField(blank=True)
    num_topics = models.IntegerField()
    num_posts = models.IntegerField()
    last_post = models.IntegerField(null=True, blank=True)
    last_post_id = models.IntegerField(null=True, blank=True)
    last_poster = models.CharField(max_length=600, blank=True)
    sort_by = models.IntegerField()
    disp_position = models.IntegerField()
    cat_id = models.IntegerField()
    class Meta:
        db_table = u'pun_forums'

class PunGroups(models.Model):
    g_id = models.IntegerField(primary_key=True)
    g_title = models.CharField(max_length=150)
    g_user_title = models.CharField(max_length=150, blank=True)
    g_read_board = models.IntegerField()
    g_post_replies = models.IntegerField()
    g_post_topics = models.IntegerField()
    g_post_polls = models.IntegerField()
    g_edit_posts = models.IntegerField()
    g_delete_posts = models.IntegerField()
    g_delete_topics = models.IntegerField()
    g_set_title = models.IntegerField()
    g_search = models.IntegerField()
    g_search_users = models.IntegerField()
    g_edit_subjects_interval = models.IntegerField()
    g_post_flood = models.IntegerField()
    g_search_flood = models.IntegerField()
    class Meta:
        db_table = u'pun_groups'

class PunOnline(models.Model):
    user_id = models.IntegerField()
    ident = models.CharField(unique=True, max_length=600)
    logged = models.IntegerField()
    idle = models.IntegerField()
    class Meta:
        db_table = u'pun_online'

class PunPosts(models.Model):
    id = models.IntegerField(primary_key=True)
    poster = models.CharField(max_length=600)
    poster_id = models.IntegerField()
    poster_ip = models.CharField(max_length=45, blank=True)
    poster_email = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True)
    hide_smilies = models.IntegerField()
    posted = models.IntegerField()
    edited = models.IntegerField(null=True, blank=True)
    edited_by = models.CharField(max_length=600, blank=True)
    topic_id = models.IntegerField()
    class Meta:
        db_table = u'pun_posts'

class PunRanks(models.Model):
    id = models.IntegerField(primary_key=True)
    rank = models.CharField(max_length=150)
    min_posts = models.IntegerField()
    class Meta:
        db_table = u'pun_ranks'

class PunReports(models.Model):
    id = models.IntegerField(primary_key=True)
    post_id = models.IntegerField()
    topic_id = models.IntegerField()
    forum_id = models.IntegerField()
    reported_by = models.IntegerField()
    created = models.IntegerField()
    message = models.TextField(blank=True)
    zapped = models.IntegerField(null=True, blank=True)
    zapped_by = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'pun_reports'

class PunSearchCache(models.Model):
    id = models.IntegerField(primary_key=True)
    ident = models.CharField(max_length=600)
    search_data = models.TextField(blank=True)
    class Meta:
        db_table = u'pun_search_cache'

class PunSearchMatches(models.Model):
    post_id = models.IntegerField()
    word_id = models.IntegerField()
    subject_match = models.IntegerField()
    class Meta:
        db_table = u'pun_search_matches'

class PunSearchWords(models.Model):
    id = models.IntegerField()
    word = models.CharField(max_length=60, primary_key=True)
    class Meta:
        db_table = u'pun_search_words'

class PunSubscriptions(models.Model):
    user_id = models.IntegerField(primary_key=True)
    topic_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'pun_subscriptions'

class PunTopics(models.Model):
    id = models.IntegerField(primary_key=True)
    poster = models.CharField(max_length=600)
    subject = models.CharField(max_length=765)
    posted = models.IntegerField()
    last_post = models.IntegerField()
    last_post_id = models.IntegerField()
    last_poster = models.CharField(max_length=600, blank=True)
    num_views = models.IntegerField()
    num_replies = models.IntegerField()
    closed = models.IntegerField()
    sticky = models.IntegerField()
    moved_to = models.IntegerField(null=True, blank=True)
    forum_id = models.IntegerField()
    class Meta:
        db_table = u'pun_topics'

class PunUsers(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    username = models.CharField(max_length=600)
    password = models.CharField(max_length=120)
    email = models.CharField(max_length=150)
    title = models.CharField(max_length=150, blank=True)
    realname = models.CharField(max_length=120, blank=True)
    url = models.CharField(max_length=300, blank=True)
    jabber = models.CharField(max_length=225, blank=True)
    icq = models.CharField(max_length=36, blank=True)
    msn = models.CharField(max_length=150, blank=True)
    aim = models.CharField(max_length=90, blank=True)
    yahoo = models.CharField(max_length=90, blank=True)
    location = models.CharField(max_length=90, blank=True)
    use_avatar = models.IntegerField()
    signature = models.TextField(blank=True)
    disp_topics = models.IntegerField(null=True, blank=True)
    disp_posts = models.IntegerField(null=True, blank=True)
    email_setting = models.IntegerField()
    save_pass = models.IntegerField()
    notify_with_post = models.IntegerField()
    show_smilies = models.IntegerField()
    show_img = models.IntegerField()
    show_img_sig = models.IntegerField()
    show_avatars = models.IntegerField()
    show_sig = models.IntegerField()
    timezone = models.FloatField()
    language = models.CharField(max_length=75)
    style = models.CharField(max_length=75)
    num_posts = models.IntegerField()
    last_post = models.IntegerField(null=True, blank=True)
    registered = models.IntegerField()
    registration_ip = models.CharField(max_length=45)
    last_visit = models.IntegerField()
    admin_note = models.CharField(max_length=90, blank=True)
    activate_string = models.CharField(max_length=150, blank=True)
    activate_key = models.CharField(max_length=24, blank=True)
    class Meta:
        db_table = u'pun_users'

