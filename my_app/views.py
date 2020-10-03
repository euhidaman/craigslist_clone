# video ==> 9:41:30
import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = "https://bangalore.craigslist.org/search/?query={}"
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


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

    # find all the elements, with the tag <li>, having class 'result-row'
    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    # Looping through all the post_listings, to extract title, url, price of the posts
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        # some, items don't have price, so if price is not found, it will print price='N/A'
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = "https://sfwallpaper.com/images/image-not-available-6.jpg"

        final_postings.append((post_title, post_url, post_price, post_image_url))

    # elements to be sent to frontend, in the form of dictionary
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
