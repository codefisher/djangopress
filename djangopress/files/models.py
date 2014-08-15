from django.db import models

class UploadedFiles(models.Model):
	upload = models.FileField(upload_to="files")

