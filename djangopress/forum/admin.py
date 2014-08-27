from django.contrib import admin
from djangopress.forum.models import Forum, ForumCategory, ForumGroup, ForumUser, Attachment, Post, Rank, Report, Thread

class ForumAdmin(admin.ModelAdmin):
    raw_id_fields = ("last_post", "subscriptions")
admin.site.register(Forum, ForumAdmin)

class ForumCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'forums')
admin.site.register(ForumCategory, ForumCategoriesAdmin)

class ForumsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
admin.site.register(ForumGroup, ForumsAdmin)

class ForumUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(ForumUser, ForumUserAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attachment, AttachmentAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'thread', 'posted', 'is_spam', 'is_public', 'is_removed')
    list_filter = ('is_spam', 'is_public', 'is_removed')
    search_fields = ('thread__subject', 'poster_name', 'author__username')
admin.site.register(Post, PostAdmin)

class RankAdmin(admin.ModelAdmin):
    pass
admin.site.register(Rank, RankAdmin)

class ReportsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Report, ReportsAdmin)

class ThreadAdmin(admin.ModelAdmin):
    pass
admin.site.register(Thread, ThreadAdmin)
