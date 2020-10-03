# video ==> 9:15:00
import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models


BASE_CRAIGSLIST_URL = "https://bangalore.craigslist.org/search/?query={}"
# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    # the get() method given below, is not POST/GET method, it's python dictionary get()
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # Append the search item entered, to the base craigslist url, in place of {}
    # so, it basically concatenates what you searched to the base url
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    post_title = post_listings[4].find(class_='result-title').text
    post_url = post_listings[4].find('a').get('href')
    post_price = post_listings[4].find(class_='result-price').text

    print(post_title)
    print(post_url)
    print(post_price)

    stuff_for_frontend = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
