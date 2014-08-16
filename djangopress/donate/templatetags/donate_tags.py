from django import template
from djangopress.donate.models import Donations

register = template.Library()

@register.inclusion_tag('donate/list.html')
def show_latest_donations(number=5):
    try:
        number = int(number)
    except ValueError:
        number = 5
    donations = Donations.objects.filter(validated=True).order_by('-date', '-amount')[0:number]
    return {
        "donations": donations,
    }
    
@register.inclusion_tag('donate/list.html')
def show_best_donations(number=5):
    try:
        number = int(number)
    except ValueError:
        number = 5
    donations = Donations.objects.filter(validated=True).order_by('-amount', '-date')[0:number]
    return {
        "donations": donations,
    }