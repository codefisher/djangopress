from django.db import models


class UploadedFile(models.Model):
    upload = models.FileField(upload_to="files/%y/%m")
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return self.upload.url