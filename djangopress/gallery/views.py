# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.utils.html import escapejs
from django.views.decorators.csrf import csrf_exempt
from .models import GallerySection, Image
from django.conf import settings

GALLERY_FONT_IMAGES = getattr(settings, 'GALLERY_FONT_IMAGES', 6)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image", )

def index(request):
	galleries = GallerySection.objects.all().order_by("position")
	images = [(gallery, Image.objects.filter(gallery=gallery)[:GALLERY_FONT_IMAGES]) for gallery in galleries]
	data = {
		"galleries": images
	}
	return render(request, 'gallery/index.html' , data)

def gallery(request, slug):
	gallery = GallerySection.objects.get(slug=slug)
	images = Image.objects.filter(gallery=gallery)
	data = {
		"gallery": gallery,
		"images": images,
	}
	return render(request, 'gallery/gallery.html' , data)

@csrf_exempt
def upload(request):
    if request.user.is_authenticated() and request.user.is_staff:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return HttpResponse("<script>window.top.django.jQuery('.mce-btn.mce-open').parent().find('.mce-textbox').val('{0}').closest('.mce-window').find('.mce-primary').click();</script>".format(image.get_absolute_url()))
        return HttpResponse("<script>alert('{0}');</script>".format(escapejs('\n'.join([v[0] for k, v in form.errors.items()]))))
    else:
        return HttpResponse("<script>alert('Access Deined');</script>")
