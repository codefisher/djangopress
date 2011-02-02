# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from djangopress.pages.models import Page

def show_page(request, path):
    page = get_object_or_404(Page, location=path)
    return render_to_response(page.template, {"page": page},
            context_instance=RequestContext(request))