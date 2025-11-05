from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    context={
        'nome_usuario':'Vitor',
        'tecnologias':['python','Django','HTML','CSS']
    }
    return render(request,'home.html',context)

def site(request):
    return HttpResponse("<h1>Nova pasta</h1>")

