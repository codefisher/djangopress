from django.contrib import admin
from djangopress.forum.models import Forum, ForumCategories, Forums, ForumUser, Attachment, Post, Rank, Reports, Thread

class ForumAdmin(admin.ModelAdmin):
    pass
admin.site.register(Forum, ForumAdmin)

class ForumCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'forums')
admin.site.register(ForumCategories, ForumCategoriesAdmin)

class ForumsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
admin.site.register(Forums, ForumsAdmin)

class ForumUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(ForumUser, ForumUserAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attachment, AttachmentAdmin)

class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)

class RankAdmin(admin.ModelAdmin):
    pass
admin.site.register(Rank, RankAdmin)

class ReportsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Reports, ReportsAdmin)

class ThreadAdmin(admin.ModelAdmin):
    pass
admin.site.register(Thread, ThreadAdmin)
