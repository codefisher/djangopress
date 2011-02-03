import datetime
from django import template
from django import forms
from djangopress.pages.models import Page
from djangopress.pages.blocks import PageBlock
from djangopress.pages.views import ShouldRedirect
register = template.Library()

def new_block_form(*args, **kargs):
    choices = [('', ' -- ')] + [(name, cls.name) for name, cls in PageBlock.sub_classes.items()]
    class NewBlockForm(forms.Form):
        content_type = forms.ChoiceField(choices=choices, required=False, initial='')
    return NewBlockForm(*args, **kargs)

class PageForm(forms.ModelForm):
    fieldsets = (
        ("Page Details", ('slug', 'title', 'override_location', 'parent')),
        ("Display Settings", ('status', 'visibility', 'login_required')),
        ("SEO Options", ('meta_page_title', 'meta_keywords', 'meta_description'))
    )
    class Meta:
        model = Page
        fields = ('slug', 'title', 'status', 'visibility', 'login_required',
                'override_location', 'parent',
                'meta_page_title', 'meta_keywords', 'meta_description')
        widgets = {
            'meta_page_title': forms.TextInput(),
            'meta_keywords': forms.Textarea(attrs={"rows": 3, "cols": 40} ),
            'meta_description': forms.Textarea(attrs={"rows": 3, "cols": 40} )
        }

def do_placeholder(parser, token):
    args = token.split_contents()
    nodelist = None
    if len(args) < 2:
        raise template.TemplateSyntaxError, "not enough arguments"
    if "with_default" in args:
        nodelist = parser.parse(('endplaceholder',))
        parser.delete_first_token()
    name = args[1][1:-1]
    return PlaceholderNode(name, nodelist, primary="primary" in args,
            identifier="identifier" in args)

class PlaceholderNode(template.Node):
    def __init__(self, name, nodelist=None, primary=False, identifier=False):
        self._nodelist = nodelist
        self._name = name
        self._primary = primary
        self._identifier = identifier

    def get_placeholder_name(self):
        return self._name

    def render(self, context):
        user = context.get('user')
        page = context.get('page')
        if self._identifier:
            blocks = PageBlock.objects.filter(block_id=self._name).order_by('position')
        else:
            blocks = page.blocks.filter(block_name=self._name).order_by('position')
        if (context.get('enable_page_edit') and user
                and user.has_perm('pages.change_page')):
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
                    else:
                        for item in form:
                            print item.label_tag(), item.errors
                else:
                    form = block.form(instance=block, prefix=prefix)
                forms.append(form)
            if changes:
                page.edited_by = user
                page.edited = datetime.datetime.now()
                page.save()
                raise ShouldRedirect()
            t = template.loader.get_template("pages/editor.html")
            context.push()
            context.update(data)
            result = t.render(context)
            context.pop()
            return result
        else:
            output = "\n".join(block.content(context) for block in blocks)
            if not output and self._nodelist:
                output = self._nodelist.render(context)
            return output

register.tag('placeholder', do_placeholder)