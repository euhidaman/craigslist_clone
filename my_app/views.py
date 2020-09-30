# video ==> 7:49:00

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'base.html')
