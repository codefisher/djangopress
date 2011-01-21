from django import template
register = template.Library()

from django.template.defaultfilters import urlencode

def url_args(args):
    if args:
        return "&".join("%s=%s" % (key, urlencode(value)) for key, value in args.items()) + "&"
    return ""

@register.inclusion_tag('util/pagination.html')
def show_pagination(pages, args=None, range_width=5):
    try:
        range_width = int(range_width)
    except ValueError:
        range_width = 5
    start = max(0, pages.number-range_width-1)
    end = min(pages.paginator.count, pages.number+range_width)
    if pages.paginator.count == 1:
        return {}
    return {
        "pages": pages,
        "range": pages.paginator.page_range[start: end],
        "args": url_args(args)
    }