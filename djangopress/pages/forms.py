from django import forms
from djangopress.pages.models import Page
from djangopress.pages.blocks import PageBlock

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