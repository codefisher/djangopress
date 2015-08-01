# Create your views here.
from django.shortcuts import render
from models import GallerySection, Image

def index(request):
	galleries = GallerySection.objects.all().order_by("position")
	images = [(gallery, Image.objects.filter(gallery=gallery)[:9]) for gallery in galleries]
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
