from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime, timedelta
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
        instruction_index = -1
        keys_list = list(request.POST.keys())
        for index, key in enumerate(keys_list):
            if key == 'special_instructions':
                instruction_index = index
                break
        context["food"] = keys_list[1:instruction_index]

        current_time = datetime.now()
        minutes = random.randint(30, 60)
        new_time = current_time + timedelta(minutes=minutes)
        formatted_time = new_time.strftime('%Y-%m-%d %H:%M:%S')
        context['time'] = formatted_time

        return render(request, template_name, context)
    
    return redirect("order")
