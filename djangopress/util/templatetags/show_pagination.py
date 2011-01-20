from django import template
register = template.Library()

@register.inclusion_tag('util/pagination.html')
def show_pagination(pages, range_width=5):
    try:
        range_width = int(range_width)
    except ValueError:
        range_width = 5
    start = max(0, pages.number-range_width-1)
    end = min(pages.paginator.count, pages.number+range_width)
    if pages.number == 1:
        return {}
    return {
        "pages": pages,
        "range": pages.paginator.page_range[start: end]
    }