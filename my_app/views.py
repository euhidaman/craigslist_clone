# video ==> 9:00:00
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup


BASE_CRAIGSLIST_URL = "https://bangalore.craigslist.org/search/sss?query={}"
# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')  # the get(), method is not POST/GET method, it's python dictionary get()
    response = requests.get('https://bangalore.craigslist.org/search/sss?query=gaming%20pc')
    data = response.text
    print(data)
    stuff_for_frontend = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
