from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms import ModelForm
from djangopress.donate.models import Donations
from django.views.decorators.csrf import csrf_exempt
import time

from paypal.standard.forms import PayPalPaymentsForm

class DonateForm(ModelForm):
    class Meta:
        model = Donations
        fields = ['name', 'link_text', 'link_url']

@csrf_exempt
def index(request):
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "item_name": "Donations to Codefisher.org",
        "invoice": "simple-donation",
        "notify_url": "https://%s" % request.get_host() + reverse('paypal-ipn'),
        "return_url": "https://%s" % request.get_host() + reverse('donate-thanks'),
        "cancel_return": "https://%s" % request.get_host() + reverse('donate-index'),
    }
    donate = DonateForm()
    form = PayPalPaymentsForm(initial=paypal_dict, button_type='donate')
    donations = Donations.objects.filter(validated=True).order_by('-amount', '-date')
    context = {"form": form, "donate": donate, "donations": donations, "title": "Donate"}
    return render(request, "donate/index.html", context)

@csrf_exempt
def thanks(request):
    return render(request, "donate/thanks.html", {"title": "Donate"})


def process(request):
    donate_form = DonateForm(request.POST)
    donate = donate_form.save()
    invoice_id = 'donate-%s-%s' % (time.strftime("%y%m%d"), donate.pk)
    donate.invoice_id = invoice_id
    donate.save()
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "item_name": "Donations to Codefisher.org",
        "invoice": invoice_id,
        "notify_url": "http://%s" % request.get_host() + reverse('paypal-ipn'),
        "return_url": "http://%s" % request.get_host() + reverse('donate-thanks'),
        "cancel_return": "http://%s" % request.get_host() + reverse('donate-index'),
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type='donate')
    context = {"form": form, "title": "Donate"}
    return render(request, "donate/process.html", context)
