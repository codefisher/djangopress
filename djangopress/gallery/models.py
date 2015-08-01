import PIL
import os
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags

# Create your models here.

class GallerySection(models.Model):
    title = models.CharField(max_length=100)
    position = models.IntegerField()
    slug = models.SlugField()
    description = models.TextField(blank=True)
    listed = models.BooleanField(default=True)

    def text_title(self):
        return strip_tags(self.title)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("gallery-gallery", kwargs={"slug": self.slug})


class Image(models.Model):
    image = models.ImageField(upload_to="images/gallery/",
                              height_field="height", width_field="width")
    thumbnail = models.ImageField(upload_to="images/gallery/thumbs/",
                                  editable=False)
    scaled = models.ImageField(upload_to="images/gallery/scaled/",
                               editable=False, null=True, blank=True)
    gallery = models.ForeignKey(GallerySection, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    def get_absolute_url(self):
        return self.image.url

    def save(self, *args, **kwargs):
        try:
            im = PIL.Image.open(self.image)
        except:
            super(Image, self).save(*args, **kwargs)
            return
        thumb = im.copy()
        im_width, im_height = thumb.size
        if 115.0 / im_width > 95.0 / im_height:
            thumb.thumbnail((115, im_height * (115.0 / im_width)),
                            PIL.Image.ANTIALIAS)
            width, height = thumb.size
            crop = int((height * (115.0 / width) - 95) / 2)
            box = (0, crop, 115, crop + 95)
            thumb = thumb.crop(box)
        else:
            thumb.thumbnail(((im_width * (95.0 / im_height)), 95),
                            PIL.Image.ANTIALIAS)
            width, height = thumb.size
            crop = int((width * (95.0 / height) - 115) / 2)
            box = (crop, 0, crop + 115, 95)
            thumb = thumb.crop(box)
        (head, tail) = os.path.split(self.image.path)
        self.thumbnail = os.path.join("images", "gallery", "thumbs", tail)
        thumbnail_path = os.path.join(head, "images", "gallery", "thumbs", tail)
        thumb.save(thumbnail_path)

        super(Image, self).save(*args, **kwargs)

        if im_width > 600 or im_height > 600:
            im.thumbnail((600, 600), PIL.Image.ANTIALIAS)
            scaled_path = os.path.join(head, "images", "gallery", "scaled", tail)
            im.save(scaled_path, quality=80)

    def scaled_image(self):
        if self.scaled:
            return self.scaled
        return self.image

    def __unicode__(self):
        return self.image.name
