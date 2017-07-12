# Create your views here.

from django import forms
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from .models import MailLog, MailAddress
from django.forms.models import modelform_factory

class ContactForm(forms.ModelForm):
    class Meta:
        model = MailLog
        fields = ('subject', 'email', 'name', 'to', 'message')

def callback(obj):
    if obj.name == 'to':
        if MailAddress.objects.count() <= 1:
            return forms.ModelChoiceField(MailAddress.objects.all(),
                initial=MailAddress.objects.first(),
                widget=forms.HiddenInput
            )
        return forms.ModelChoiceField(
            MailAddress.objects.all(),
            initial=MailAddress.objects.first())
    return obj.formfield()

def contact(request):
    error = None
    contact_form = modelform_factory(MailLog, form=ContactForm, formfield_callback=callback)
    if request.method == 'POST':
        form = contact_form(request.POST)
        if form.is_valid():
            mail_entry = form.save()
            try:
                result = send_mail(mail_entry.subject,
                          mail_entry.message,
                          "{0} <{1}>".format(mail_entry.name, mail_entry.email),
                          [mail_entry.to.email], fail_silently=False)
                if result:
                    return redirect(reverse(thanks))
                else:
                    error = "A mail server error caused the sending of mail to fail, please try again later."
            except:
                error = "A server error caused the sending of mail to fail, please try again later."
    else:
        form = contact_form()
    return render(request, "contact/index.html", {"form": form, "title": "Contact", "error": error})

def thanks(request):
    return render(request, "base.html", 
                  {"title": "Contact", "page_header": "Thank You", 
                   "page_message": "Thank you for taking the time to send me an email, I will try and get back to you as soon as possible."})
