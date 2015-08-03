from django import forms
from django.http import HttpResponse

from django.utils.html import escapejs
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile

class ImageForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ("upload", )

@csrf_exempt
def upload(request):
    if request.user.is_authenticated() and request.user.is_staff:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return HttpResponse("<script>window.top.django.jQuery('.mce-btn.mce-open').parent().find('.mce-textbox').val('{0}');</script>".format(image.get_absolute_url()))
        return HttpResponse("<script>alert('{0}');</script>".format(escapejs('\n'.join([v[0] for k, v in form.errors.items()]))))
    else:
        return HttpResponse("<script>alert('Access Deined');</script>")
