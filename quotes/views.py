from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

# def home(request):
#     '''A function to respond to the /hw URL.
#     '''
#     # create some text:
#     response_text = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>
#     This is our first django web page!
#     </p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     '''
#     # return a response to the client
#     return HttpResponse(response_text)

image_list = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZV_TPSJgiLFnpZWLkG-tuDTxfNIVnZZ-AFA&s",
              "https://www.thephilroom.com/wp-content/uploads/2022/10/Sun-tzu.png",
              "https://pbs.twimg.com/profile_images/1434814659907964929/8DbrEI_o_400x400.jpg",
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCWEhRk6Nk4UYHNmOsUqvr0o9QZfNzC4NZow&s",
              "https://t4.ftcdn.net/jpg/05/66/86/23/360_F_566862317_vsNNyMksfdJ70vJpNjb7h057a7ctUi1C.jpg"]
sun_tzu_quotes = [
    "The supreme art of war is to subdue the enemy without fighting.",
    "All warfare is based on deception.",
    "Victorious warriors win first and then go to war, while defeated warriors go to war first and then seek to win.",
    "In the midst of chaos, there is also opportunity.",
    "Know thyself, know thy enemy. A thousand battles, a thousand victories.",
    "Appear weak when you are strong, and strong when you are weak.",
    "The greatest victory is that which requires no battle.",
    "He who knows when to fight and when not to fight will win.",
    "Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt.",
    "The wise warrior avoids the battle.",
    "Opportunities multiply as they are seized."
]

def quote(request):
    '''
    A function to respond to the /quotes/quote URL.
    This function will display a random quote
    '''
    template_name = "quotes/quote.html"
    context = {
        'image_src' : image_list[random.randint(0,4)],
        'quote_src' : sun_tzu_quotes[random.randint(0,10)]
    }
    return render(request, template_name, context)

def show_all(request):
    '''
    A function to respond to the /quotes/show_all URL.
    This function will display all images and quotes
    '''
    template_name = "quotes/show_all.html"
    context = {
        'image_list' : image_list,
        'quote_list' : sun_tzu_quotes
    }
    return render(request, template_name, context)

def about(request):
    '''
    A function to respond to the /hw/about URL.
    This function will delegate work to an HTML template.
    '''
    # this template will present the response
    template_name = "quotes/about.html"

    # delegate response to the template:
    return render(request, template_name)