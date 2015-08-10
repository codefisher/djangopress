import PIL
import os
import re
from lxml import html
from django.db import models
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from djangopress.core.format.html import Library

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
        return strip_tags(self.title)

    def get_absolute_url(self):
        return reverse("gallery-gallery", kwargs={"slug": self.slug})


class Image(models.Model):
    image = models.ImageField(upload_to="images/gallery/%y/%m/",
                              height_field="height", width_field="width")
    thumbnail = models.ImageField(upload_to="images/gallery/thumbs/%y/%m/",
                                  editable=False, null=True, blank=True)
    scaled = models.ImageField(upload_to="images/gallery/scaled/%y/%m/",
                               editable=False, null=True, blank=True)
    gallery = models.ForeignKey(GallerySection, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return self.image.url

    def ensure_folder(self, path):
        folder = os.path.dirname(path)
        try:
            os.makedirs(folder)
        except OSError:
            pass

    def save(self, *args, **kwargs):
        try:
            im = PIL.Image.open(self.image)
        except:
            super(Image, self).save(*args, **kwargs)
            return

        super(Image, self).save(*args, **kwargs)

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
        path_match = re.match(r'(.+?)((\d+/\d+/)?[^/]+)$', self.image.path)
        head, tail = path_match.group(1), path_match.group(2)
        self.thumbnail = os.path.join("images", "gallery", "thumbs", tail)
        thumbnail_path = os.path.join(head, "thumbs", tail)
        self.ensure_folder(thumbnail_path)
        thumb.save(thumbnail_path)

        if im_width > 600 or im_height > 600:
            im.thumbnail((600, 600), PIL.Image.ANTIALIAS)
            self.scaled = os.path.join("images", "gallery", "scaled", tail)
            scaled_path = os.path.join(head, "scaled", tail)
            self.ensure_folder(scaled_path)
            im.save(scaled_path, quality=80)

        super(Image, self).save(*args, **kwargs)

    def scaled_image(self):
        if self.scaled:
            return self.scaled
        return self.image

    def __unicode__(self):
        return self.image.name

def gallery(node):
    gallery_id = node.attrib.get('id')
    show_description = node.attrib.get('show_description', False)
    show_title = node.attrib.get('show_title', False)
    gallery = GallerySection.objects.get(pk=gallery_id)
    images = Image.objects.filter(gallery=gallery)
    if node.attrib.get('count'):
        images = images[0:int(node.attrib.get('count'))]
    data = {
        "gallery": gallery,
        "images": images,
        "show_description": show_description,
        "show_title": show_title
    }
    return html.fromstring(render_to_string("gallery/tag.html", data))

Library.tag("//gallery", gallery)