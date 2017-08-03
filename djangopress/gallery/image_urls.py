from django.conf.urls import url
from .views import crop, resize

"""
These can help with the serving of images as a dynamic size.
"""

urlpatterns = [
    url(r'^crop/(?P<width>\d+)x(?P<height>\d+)/(?P<image>.+)', crop,
        name='gallery-crop'),
    url(r'^resize/(?P<width>\d+)x(?P<height>\d+)/(?P<image>.+)', resize,
        name='gallery-resize'),
    url(r'^resize/(?P<width>\d+)w/(?P<image>.+)', resize, name='gallery-resize'),
    url(r'^resize/(?P<height>\d+)h/(?P<image>.+)', resize, name='gallery-resize'),
]