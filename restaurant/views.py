from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

def main(request):
    '''
    A function to respond to the /restaurant/main URL.
    This function will display a random quote
    '''
    template_name = "restaurant/main.html"
    return render(request, template_name)

def order(request):
    '''
    A function to respond to the /restaurant/order URL.
    This function will display all images and quotes
    '''
    template_name = "restaurant/order.html"
    return render(request, template_name)

def confirmation(request):
    '''
    A function to respond to the /restaurant/confirmation URL.
    This function will delegate work to an HTML template.
    '''
    template_name = 'restaurant/confirmation.html'
    if request.POST:

        # read the form data into python variables:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_instructions = request.POST['special_instructions']
        context = {
            "name": name,
            "phone": phone,
            "email": email,
            "special_instructions": special_instructions
        }
        return render(request, template_name, context)

    ## GET lands down here: no return statements!

    # this is an OK solution: a graceful failure
    # return HttpResponse("Nope.")

    # if the client got here by making a GET on this URL, send back the form
    # use this template to produce the response

    # this is a "better solution", but shows the wrong URL
    # template_name = 'formdata/form.html'
    # return render(request, template_name)

    # this is the "best" solution: redirect to the correct URL
    return redirect("order")