from django.contrib import admin
from djangopress.files.models import UploadedFile
from django.contrib.sites.models import Site

class UploadAdmin(admin.ModelAdmin):
    list_display = ('upload', 'upload_url', 'description', 'date')

    def upload_url(self, upload):
        site = Site.objects.get_current()
        path = "http://{0}{1}".format(site.domain, upload.upload.url)
        return '<a href="{0}">{1}</a>'.format(upload.upload.url, path)
    upload_url.allow_tags = True

admin.site.register(UploadedFile, UploadAdmin)
