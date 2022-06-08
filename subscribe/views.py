from django.shortcuts import render
from globomantics.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail

# Create your views here.
#DataFlair #Send Email
#https://support.google.com/accounts/answer/185833
def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome to DataFlair'
        message = 'Hope you are enjoying your Django Tutorials'
        recipient = str(sub['Email'].value())
        send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently = False)
        return render(request, 'subscribe/success.html', {'recipient': recipient})
    return render(request, 'subscribe/index.html', {'form':sub})