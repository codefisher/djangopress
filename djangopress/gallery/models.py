from lxml import html
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from djangopress.core.format.html import Library
from django.conf import settings

GALLERY_SETTINGS = getattr(settings, 'GALLERY_SETTINGS', {
    "sizes": {
        "thumb": {
            "mode": "gallery-crop",
            "width": 115,
            "height": 95
        },
        "scaled": {
            "mode": "gallery-resize",
            "width": 1200,
            "height": 1200
        },
        "slider": {
            "mode": "gallery-crop",
            "width": 870,
            "height": 410
        }
    }
})

class Thumber(object):
    def __init__(self, width=None, height=None):
        self._width = width
        self._height = height

    @property
    def width(self):
        if self._width:
            return self._width
        sizes = GALLERY_SETTINGS.get("sizes").get("thumb")
        return sizes.get('width')

    @property
    def height(self):
        if self._height:
            return self._height
        sizes = GALLERY_SETTINGS.get("sizes").get("thumb")
        return sizes.get('height')

    def thumb(self, image):
        sizes = GALLERY_SETTINGS.get("sizes").get("thumb")
        return reverse(sizes.get("mode"), kwargs={
            "image": image.image.name,
            "width": self.width,
            "height": self.height
        })

class GallerySection(models.Model):
    title = models.CharField(max_length=100)
    position = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    listed = models.BooleanField(default=True)

    def text_title(self):
        return strip_tags(self.title)

    def __str__(self):
        return strip_tags(self.title)

    def get_absolute_url(self):
        return reverse("gallery-gallery", kwargs={"slug": self.slug})

    def as_html(self, count=None, show_description=False,
                show_title=False, slider=False, thumber=None):
        if not thumber:
            thumber = Thumber()
        images = Image.objects.filter(
            gallery=self).order_by('position', '-date')
        if count:
            images = images[0:int(count)]
        data = {
            "gallery": self,
            "images": images,
            "show_description": show_description,
            "show_title": show_title,
            "thumber": thumber
        }
        if slider:
            template = "gallery/slider.html"
        else:
            template = "gallery/tag.html"
        return render_to_string(template, data)


class Image(models.Model):
    image = models.ImageField(upload_to="images/gallery/%y/%m/",
                              height_field="height", width_field="width")
    gallery = models.ForeignKey(GallerySection, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)
    date = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(default=0)

    def get_absolute_url(self):
        return self.image.url

    @property
    def thumbnail(self):
        sizes = GALLERY_SETTINGS.get("sizes").get("thumb")
        return reverse(sizes.get("mode"), kwargs={
            "image": self.image.name,
            "width": sizes.get("width"),
            "height": sizes.get("height")
        })

    @property
    def scaled(self):
        sizes = GALLERY_SETTINGS.get("sizes").get("scaled")
        return reverse(sizes.get("mode"), kwargs={
            "image": self.image.name,
            "width": sizes.get("width"),
            "height": sizes.get("height")
        })

    @property
    def slider(self):
        sizes = GALLERY_SETTINGS.get("sizes").get("slider")
        return reverse(sizes.get("mode"), kwargs={
            "image": self.image.name,
            "width": sizes.get("width"),
            "height": sizes.get("height")
        })

    def __str__(self):
        return self.image.name

def gallery(node):
    gallery_id = node.attrib.get('id')
    show_description = node.attrib.get('show_description', False)
    show_title = node.attrib.get('show_title', False)
    count = node.attrib.get('count')
    slider = node.attrib.get('slider', False)
    gallery = GallerySection.objects.get(pk=gallery_id)
    return  html.fromstring(gallery.as_html(count=count, show_description=show_description,
                show_title=show_title, slider=slider))

Library.tag("//gallery", gallery)