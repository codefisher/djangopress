from django.db import models

class Link(models.Model):
    location = models.TextField(blank=True, null=False)
    label_text = models.CharField(max_length=100, blank=True, null=False)

    def label(self):
        return self.label_text

    def get_absolute_url(self):
        return self.location
    
    def __str__(self):
        return self.location