# Create your views here.

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from djangopress.settings import ADMINS
from django.core.urlresolvers import reverse

class ContactForm(forms.Form):
    subject = forms.CharField(label="Subject")
    email = forms.EmailField(label="Email")
    name = forms.CharField(label="Name")
    message = forms.CharField(widget=forms.Textarea)
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_mail(form.cleaned_data['subject'], 
                          form.cleaned_data['message'], 
                          "%s <%s>" % (form.cleaned_data['name'], form.cleaned_data['email']),
                          [email for name, email in ADMINS], fail_silently=False)
                return HttpResponseRedirect(reverse(thanks))
            except:
                pass
    else:
        form = ContactForm()
    return render(request, "contact/index.html", {"form": form, "title": "Contact"})

def thanks(request):
    return render(request, "base.html", 
                  {"title": "Contact", "page_header": "Thanks You", 
                   "message": "Thank you for taking the time to send me an email"})
