from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def xyz(request):
    return render(request, "index.html")


def signup(request):
    i=10
    i=i+20
    i=i+30
    return render(request, "index.html")
