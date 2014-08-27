from django import template
register = template.Library()

@register.simple_tag()
def _page_link(instance, page):
    return instance.get_absolute_url(page=page)

@register.inclusion_tag('core/pagination.html')
def show_pagination(pages, instance, range_width=3):
    return _show_pagination(pages, instance, range_width)
    
@register.inclusion_tag('core/simple_pagination.html')
def simple_pagination(pages, instance, range_width=3):
    return _show_pagination(pages, instance, range_width)

def _show_pagination(pages, instance, range_width=3):
    try:
        range_width = int(range_width)
    except ValueError:
        range_width = 3
    page = pages.number
    num_pages = pages.paginator.num_pages
    if num_pages == 1:
        return {}
    temp_range = list(range(1,min(num_pages+1, range_width+1)))+list(range(min(page-range_width+2, num_pages-range_width), min(page+range_width-1, num_pages+1)))+list(range(num_pages-range_width+1,num_pages+1))
    page_range = []
    for i in temp_range:
        if not page_range:
            page_range.append(i)
        elif i <= page_range[-1]:
            continue
        elif i > page_range[-1]+1:
            page_range.append(None)
            page_range.append(i)
        else:
            page_range.append(i)
    return {
        "pages": pages,
        "instance": instance,
        "range": page_range,
    }