from django.shortcuts import render, redirect
from .forms import PurchaseForm
from django.http import HttpResponseRedirect, HttpResponse
import random
from django.core.cache import cache
from twilio.rest import Client
from earnWhileShop import settings
from django.views.decorators.debug import sensitive_variables


@sensitive_variables('url')
def shopping(request):
    if request.method == 'POST':
        f = PurchaseForm(request.POST)
        if f.is_valid():
            url = request.POST.get("link") + "&tag=" + settings.AMAZON_ASSOCIATE_KEY
            return HttpResponseRedirect(url)
        return render(request, 'Shopping/shopping.html', {'form':f,})
    return render(request, 'Shopping/shopping.html', {'form':PurchaseForm(),})


def _get_pin(length=5):
    """ Return a numeric PIN with length digits """
    return random.sample(range(10**(length-1), 10**length), 1)[0]


def _verify_pin(mobile_number, pin):
    """ Verify a PIN is correct """
    return pin == cache.get(mobile_number)


def ajax_send_pin(request):
    """ Sends SMS PIN to the specified number """
    mobile_number = request.POST.get('paytm_number', "")
    if not mobile_number:
        return HttpResponse("No mobile number", status=403)
    try:
        pin = _get_pin()

        # store the PIN in the cache for later verification.
        cache.set(mobile_number, pin, 600) # valid for 10 minutes
        client = Client(settings.TWILIO_ACCOUNT_SID_KEY, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
                            body="%s" % pin,
                            to=mobile_number,
                            from_=settings.SECRET_TWILIO_FROM_NUMBER,
                        )
        return HttpResponse("Message sent")
    except:
        return HttpResponse("Please check the phone number")


def process_order(request):
    """ Process orders made via web form and verified by SMS PIN. """
    form = PurchaseForm(request.POST or None)

    if form.is_valid():
        pin = int(request.POST.get("pin", "0"))
        mobile_number = request.POST.get("mobile_number", "")

        if _verify_pin(mobile_number, pin):
            form.save()
            return redirect('transaction_complete')
        else:
            messages.error(request, "Invalid PIN!")
    else:
        return render(
                    request,
                    'order.html',
                    {
                        'form': form
                    }
                )