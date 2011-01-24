from django.forms import fields

from django import template
register = template.Library()

@register.inclusion_tag('util/form.html')
def form(pages, form):
    return {
        "form": form
    }

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, fields.CheckboxInput)

@register.inclusion_tag('util/field_form.html')
def field_form(form, action=None):
    if not action:
        action = "."
    fieldsets = []
    errors = []
    fields_map =  dict((field.name, field) for field in form)
    form_fields = []
    for legend, fields in form.fieldsets:
        set_fields = [fields_map.get(field) for field in fields]
        fieldsets.append((legend, set_fields))
        form_fields.extend(set_fields)
        errors.extend((field for field in set_fields if field.errors))
    return {
        "form": form,
        "fieldsets": fieldsets,
        "fields": form_fields,
        "errors": errors,
        "action": action,
    }
