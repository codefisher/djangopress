import time
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.forms import ModelForm
from djangopress.donate.models import Donation
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

class DonationPayPalPaymentsForm(PayPalPaymentsForm):

    def render(self):
        return mark_safe(u"""<form action="%s" method="post">
        %s
        <input type="image" src="%s" style="border:0;" name="submit" alt="Buy it Now" />
        </form>""" % (self.get_endpoint(), self.as_p(), self.get_image()))

class DonateForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'link_text', 'link_url']

@csrf_exempt
def index(request):
    if request.method == 'POST':
        donate_form = DonateForm(request.POST)
        if donate_form.is_valid():
            donate = donate_form.save()
            invoice_id = 'donate-%s-%s' % (time.strftime("%y%m%d"), donate.pk)
            donate.invoice_id = invoice_id
            donate.save()
        
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "item_name": "Donation to Codefisher.org",
                "invoice": invoice_id,
                "notify_url": "http://%s" % request.get_host() + reverse('paypal-ipn'),
                "return_url": "http://%s" % request.get_host() + reverse('donate-thanks'),
                "cancel_return": "http://%s" % request.get_host() + reverse('donate-index'),
            }
            # Create the instance.
            form = DonationPayPalPaymentsForm(initial=paypal_dict, button_type='donate')
            context = {"form": form, "title": "Donate"}
            return render(request, "donate/process.html", context)
    else:
        donate_form = DonateForm()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "item_name": "Donation to Codefisher.org",
        "invoice": "simple-donation-%s" % time.strftime("%y%m%d%H%M%S"),
        "notify_url": "https://%s" % request.get_host() + reverse('paypal-ipn'),
        "return_url": "https://%s" % request.get_host() + reverse('donate-thanks'),
        "cancel_return": "https://%s" % request.get_host() + reverse('donate-index'),
    }
   
    form = DonationPayPalPaymentsForm(initial=paypal_dict, button_type='donate')
    donations = Donation.objects.filter(validated=True).order_by('-amount', '-date')
    context = {"form": form, "donate": donate_form, "donations": donations, "title": "Donate"}
    return render(request, "donate/index.html", context)

@csrf_exempt
def thanks(request):
    return render(request, "donate/thanks.html", {"title": "Donate"})