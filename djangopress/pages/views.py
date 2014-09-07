# Create your views here.

from django.shortcuts import render, get_object_or_404
from djangopress.pages.models import Page, PageBlock
from django.conf import settings
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from djangopress.pages.forms import PageForm, NewBlockForm, TextForm


def show_page(request, path):
    try:
        page = Page.objects.get(location=path, sites__id__exact=settings.SITE_ID,
                visibility="VI", status="PB")
    except:
        raise Http404
    if hasattr(request, 'user'):
        user = request.user
        show_toolbar = user.has_perm('pages.change_page') if user else False
    else:
        show_toolbar = False
    data = {
        "page": page,
        "show_toolbar": show_toolbar,
        "enable_page_edit": "edit_cms_page" in request.GET
    }
    return render(request, page.template.template, data)

def get_blocks(page, identifier, name):
    if identifier:
        return PageBlock.objects.filter(block_id=identifier)
    else:
        return page.blocks.filter(block_name=name)

def get_forms(blocks, name):
    forms = []
    for block in blocks:
        form = TextForm(instance=block, prefix="%s-%s" % (block.pk, name))
        forms.append(form)
    return forms

def page_edit(request, identifier=None, name=None, page=None,
        template_name='pages/editor/block.html'):
    if not request.user.has_perm('pages.change_page'):
        return HttpResponseForbidden()
    page = get_object_or_404(Page, pk=page)

    blocks = get_blocks(page, identifier, name)
    forms = []
    changes = False
    if request.method == 'POST':
        new_block = NewBlockForm(request.POST, prefix=name)
        if new_block.is_valid():
            block = PageBlock(block_name=name, block_id=identifier, position=blocks.count()+1, page=page)
            block.save()
            blocks = get_blocks(page, identifier, name)
            forms = get_forms(blocks, name)
        else:
            for block in blocks:
                prefix = "%s-%s" % (block.pk, name)
                form = TextForm(request.POST, instance=block, prefix=prefix)
                if form.is_valid():
                    form.save(True)
                    changes = True
                else:
                    form = TextForm(instance=block, prefix=prefix)
                forms.append(form)
            print changes
            if changes:
                return HttpResponseRedirect(page.location)
    else:
        forms = get_forms(blocks, name)
    new_block = NewBlockForm(prefix=name)
    data = {
        "page": page,
        "forms": forms,
        "new_block": new_block,
        "name": identifier if identifier else name,
    }
    return render(request, template_name, data)

def page_edit_ajax(request):
    if not request.user.has_perm('pages.change_page'):
        return HttpResponseForbidden()
    action = request.GET.get("action")
    if action == 'edit-page':
        return page_edit_details(request, request.GET.get("page"),
                template_name='pages/editor/details-form.html')
    elif action == 'edit-block':
        return page_edit(request, request.GET.get("identifier"),
                  request.GET.get("name"), request.GET.get("page"),
                  template_name='pages/editor/block-form.html')
    raise Http404

def page_edit_details(request, page, template_name='pages/editor/details.html'):
    if not request.user.has_perm('pages.change_page'):
        return HttpResponseForbidden()
    page = get_object_or_404(Page, pk=page)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page, prefix="page-primary")
        if form.is_valid():
            form.save(True)
            return HttpResponseRedirect(page.location)
    else:
        form = PageForm(instance=page, prefix="page-primary")
    data = {
        "page": page,
        "form": form,
    }
    return render(request, template_name, data)

def page_edit_js(request, template_name='pages/js/edit-page.js'):
    if not request.user.has_perm('pages.change_page'):
        return HttpResponseForbidden()
    return render(request, template_name, content_type="text/javascript")