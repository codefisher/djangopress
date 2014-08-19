# Create your views here.

from django.shortcuts import render, get_object_or_404
from djangopress.pages.models import Page, PageBlock
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from djangopress.pages.forms import PageForm, new_block_form


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
    return render(request, page.template, data)

def get_blocks(page, identifier, name):
    if identifier:
        return PageBlock.objects.filter(block_id=identifier)
    else:
        return page.blocks.filter(block_name=name)

def get_forms(blocks, name):
    forms = []
    for block in blocks:
        block = block.get_child()
        form = block.form(instance=block, prefix="%s-%s" % (block.pk, name))
        forms.append(form)
    return forms

def page_edit(request, identifier=None, name=None, page=None,
        template_name='pages/editor/block.html'):
    page = get_object_or_404(Page, pk=page)

    blocks = get_blocks(page, identifier, name)
    forms = []
    changes = False
    if request.method == 'POST':
        new_block = new_block_form(request.POST, prefix=name)
        if new_block.is_valid() and new_block.cleaned_data.get('content_type'):
            content_type = new_block.cleaned_data.get('content_type')
            block = PageBlock.sub_classes[content_type](block_name=name, block_id=identifier, position=blocks.count()+1)
            block.save()
            page.blocks.add(block)
            blocks = get_blocks(page, identifier, name)
            forms = get_forms(blocks, name)
        else:
            for block in blocks:
                block = block.get_child()
                prefix = "%s-%s" % (block.pk, name)
                form = block.form(request.POST, instance=block, prefix=prefix)
                if form.is_valid():
                    form.save(True)
                    changes = True
                else:
                    form = block.form(instance=block, prefix=prefix)
                forms.append(form)
            print changes
            if changes:
                return HttpResponseRedirect(page.location)
    else:
        forms = get_forms(blocks, name)
    new_block = new_block_form(prefix=name)
    data = {
        "page": page,
        "forms": forms,
        "new_block": new_block,
        "name": identifier if identifier else name,
    }
    return render(request, template_name, data)

def page_edit_ajax(request):
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
    return render(request, template_name, mimetype="text/javascript")

'''
            request = context.get('request')
            submit_name = "%s-submit" % self._name
            forms = []
            created = False
            if (request.method == 'POST'
                    and submit_name in request.POST):
                new_block = new_block_form(request.POST, prefix=self._name)
                if new_block.is_valid():
                    content_type = new_block.cleaned_data['content_type']
                    if content_type:
                        block = PageBlock.sub_classes[content_type](block_name=self._name, position=blocks.count()+1)
                        block.save()
                        page.blocks.add(block)
                        if self._identifier:
                            blocks = PageBlock.object.filter(block_id=self._name).order_by('position')
                        else:
                            blocks = page.blocks.filter(block_name=self._name).order_by('position')
                        created = True
            new_block = new_block_form(prefix=self._name)
            data = {
                "forms": forms,
                "new_block": new_block,
                "submit_name": submit_name
            }
            changes = False
            if self._primary:
                if (request.method == 'POST'
                        and submit_name in request.POST):
                    form = PageForm(request.POST, instance=page, prefix="page-primary")
                    if form.is_valid():
                        form.save(True)
                        changes = True
                else:
                    form = PageForm(instance=page, prefix="page-primary")
                data["primary_form"] = form
            for block in blocks:
                block = block.get_child()
                prefix = "%s-%s" % (block.pk, self._name)
                if (request.method == 'POST' and not created
                        and submit_name in request.POST):
                    form = block.form(request.POST, instance=block, prefix=prefix)
                    if form.is_valid():
                        form.save(True)
                        changes = True
                else:
                    form = block.form(instance=block, prefix=prefix)
                forms.append(form)
            if changes or created:
                page.edited_by = user
                page.edited = datetime.datetime.now()
                page.save()
                raise ShouldRedirect()
            return render_to_string("pages/editor.html", data, context_instance=context)
'''