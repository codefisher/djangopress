from django.contrib import admin
from djangopress.files.models import UploadedFiles
from django.contrib.sites.models import Site

class UploadAdmin(admin.ModelAdmin):
	list_display = ('upload', 'upload_url')

	def upload_url(self, upload):
		site = Site.objects.get_current()
		return "http://%s%s" % (site, upload.upload.url)

admin.site.register(UploadedFiles, UploadAdmin)
