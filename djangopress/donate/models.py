from django.db import models
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.ipn.models import PayPalIPN
import datetime

class Donation(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(default=datetime.datetime.today)
    amount = models.DecimalField(blank=True, default=0, max_digits=6, decimal_places=2)
    link_url = models.URLField(blank=True, null=True, verbose_name="Link Url (optional)")
    link_text = models.CharField(max_length=50, blank=True, null=True, verbose_name="Link Text (optional)")
    validated = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=50, null=True, blank=True)
    payment = models.ForeignKey(PayPalIPN, null=True, blank=True, on_delete=models.CASCADE)

def update_donation(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":
        # Undertake some action depending upon `ipn_obj`.
        try:
            donation = Donation.objects.get(invoice_id=ipn_obj.invoice)
        except Donation.DoesNotExist:
            return
        donation.validated = True
        donation.amount = ipn_obj.mc_gross
        donation.payment = ipn_obj
        donation.save()
    else:
        pass # not a good payment
valid_ipn_received.connect(update_donation)