from django.forms import fields
from django import forms

from django import template
register = template.Library()

@register.inclusion_tag('core/form.html')
def form(form):
    return {
        "form": form
    }

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, fields.CheckboxInput)

@register.filter(name='is_textarea')
def is_textarea(value):
    return isinstance(value, forms.Textarea)

@register.inclusion_tag('core/field_form.html')
def field_form(form, action=None, full=True):
    if not action:
        action = "."
    fieldsets = []
    errors = []
    fields_map =  dict((field.name, field) for field in form)
    form_fields = []

    for legend, fields in form.fieldsets:
        try:
            set_fields = [fields_map.get(field) for field in fields]
            fieldsets.append((legend, set_fields))
            form_fields.extend(set_fields)
            errors.extend((field for field in set_fields if field.errors))
        except:
            pass
    return {
        "form": form,
        "fieldsets": fieldsets,
        "fields": form_fields,
        "errors": errors,
        "action": action,
        "full": full,
    }
