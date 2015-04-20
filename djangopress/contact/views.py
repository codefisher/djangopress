# Create your views here.

from django import forms
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse

class ContactForm(forms.Form):
    subject = forms.CharField(label="Subject")
    email = forms.EmailField(label="Email")
    name = forms.CharField(label="Name")
    message = forms.CharField(widget=forms.Textarea)
    
def contact(request):
    error = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
    if form.is_valid():
            try:
                result = send_mail(form.cleaned_data['subject'], 
                          form.cleaned_data['message'], 
                          "%s <%s>" % (form.cleaned_data['name'], form.cleaned_data['email']),
                          [email for name, email in settings.ADMINS], fail_silently=False)
                if result:
                    return redirect(reverse(thanks))
                else:
                    error = "A mail server error caused the sending of mail to fail, please try again later."
            except:
                error = "A server error caused the sending of mail to fail, please try again later."
    else:
        form = ContactForm()
    return render(request, "contact/index.html", {"form": form, "title": "Contact", "error": error})

def thanks(request):
    return render(request, "base.html", 
                  {"title": "Contact", "page_header": "Thank You", 
                   "page_message": "Thank you for taking the time to send me an email, I will try and get back to you as soon as possible."})
