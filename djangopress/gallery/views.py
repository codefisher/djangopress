import os
import PIL
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django import forms
from django.utils.html import escapejs
from django.views.decorators.csrf import csrf_exempt
from .models import GallerySection, Image
from django.conf import settings

GALLERY_FRONT_IMAGES = getattr(settings, 'GALLERY_FRONT_IMAGES', 6)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image",)


def index(request):
    galleries = GallerySection.objects.filter(listed=True).order_by(
        "position")
    images = [(gallery,
               Image.objects.filter(gallery=gallery
                                    ).order_by('position', '-date')[
               :GALLERY_FRONT_IMAGES]) for gallery in galleries]
    data = {
        "galleries": images
    }
    return render(request, 'gallery/index.html', data)


def gallery(request, slug):
    try:
        gallery = GallerySection.objects.get(slug=slug)
    except GallerySection.DoesNotExist:
        raise Http404
    images = Image.objects.filter(gallery=gallery).order_by('position', '-date')
    data = {
        "gallery": gallery,
        "images": images,
    }
    return render(request, 'gallery/gallery.html', data)


@csrf_exempt
def upload(request):
    if request.user.is_authenticated() and request.user.is_staff:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return HttpResponse(
                "<script>window.top.django.jQuery('.mce-btn.mce-open').parent().find('.mce-textbox').val('{0}');</script>".format(
                    image.get_absolute_url()))
        return HttpResponse("<script>alert('{0}');</script>".format(
            escapejs('\n'.join([v[0] for k, v in form.errors.items()]))))
    else:
        return HttpResponse("<script>alert('Access Denied');</script>")


def size_image(request, image, width, height, sizer):
    path = os.path.join(settings.MEDIA_ROOT, image)
    out_file = os.path.join(settings.MEDIA_ROOT,
                            request.path.lstrip(settings.MEDIA_URL))
    out_folder = os.path.dirname(out_file)
    if not os.path.exists(out_file):
        try:
            im = PIL.Image.open(path)
        except FileNotFoundError as e:
            raise Http404
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
        img_width, img_height = im.size
        if width is None:
            width = img_width
        if height is None:
            height = img_height
        width = int(width)
        height = int(height)
        sizer(im, width, height, out_file)
        im.close()
    if settings.DEBUG:
        with open(out_file, 'rb') as fp:
            response = HttpResponse(content=fp)
            content_type, encodeing = mimetypes.guess_type(out_file)
            response['Content-Type'] = content_type
    else:
        # we assume nginx, we just tell it to request the file which is now saved
        responce = HttpResponse()
        responce["X-Accel-Redirect"] = request.path
    return response


def crop(request, image, width, height):
    def sizer(im, width, height, out_file):
        img_width, img_height = im.size
        if width / img_width > height / img_height:
            new_height = int(img_height * width / img_width)
            im = im.resize((width, new_height), PIL.Image.ANTIALIAS)
            diff = (new_height - height) / 2
            im = im.crop((0, diff, width, new_height - diff))
        else:
            new_width = int(img_width * height / img_height)
            im = im.resize((new_width, height), PIL.Image.ANTIALIAS)
            diff = (new_width - width) / 2
            im = im.crop((diff, 0, new_width - diff, height))
        im.save(out_file)

    return size_image(request, image, width, height, sizer)


def resize(request, image, width=None, height=None):
    def sizer(im, width, height, out_file):
        im.thumbnail((width, height), PIL.Image.ANTIALIAS)
        im.save(out_file)

    return size_image(request, image, width, height, sizer)
