from django.db import models
from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.models import PayPalIPN
import datetime

# Create your models here.

class Donation(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(default=datetime.datetime.today)
    amount = models.FloatField(blank=True, default=0)
    link_url = models.URLField(blank=True, null=True)
    link_text = models.CharField(max_length=50, blank=True, null=True)
    validated = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=50, null=True, blank=True)
    payment = models.ForeignKey(PayPalIPN, null=True, blank=True)

def update_donation(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":
        # Undertake some action depending upon `ipn_obj`.
        donation = Donation.objects.get(invoice_id=ipn_obj.invoice)
        if donation:
            donation.validated = True
            donation.amount = ipn_obj.auth_amount
            donation.payment = ipn_obj
            donation.save()
    else:
        pass # not a good payment
payment_was_successful.connect(update_donation)