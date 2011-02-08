# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from djangopress.pages.models import Page
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django import template

class ShouldRedirect(template.TemplateSyntaxError):
    pass

def show_page(request, path):
    try:
        page = Page.objects.get(location=path, sites__id__exact=settings.SITE_ID,
                visibility="VI", status="PB")
    except:
        raise Http404
    user = request.user
    show_toolbar = user.has_perm('pages.change_page') if user else False
    data = {
        "page": page,
        "show_toolbar": show_toolbar,
        "enable_page_edit": "edit_cms_page" in request.GET
    }
    try:
        return render_to_response(page.template, data,
                context_instance=RequestContext(request))
    except ShouldRedirect:
        return HttpResponseRedirect(page.location)