from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request, 'home.html')
def site(request):
    return HttpResponse("<h1>Nova pasta</h1>")