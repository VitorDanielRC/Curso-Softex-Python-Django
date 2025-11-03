from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("<h1>Olá,Mundo! Esta e minha primeira pagina Django!</h1>")

def site(request):
    return HttpResponse("<h1>Nova pasta</h1>")