from django.shortcuts import render
from django.http import HttpResponse
from .models import Tarefa
from .models import execucao
# Create your views here.
def home(request):
    todas_as_tarefas = Tarefa.objects.all()
    execucao_as = execucao.objects.all()
    context={
        'nome_usuario':'Vitor',
        'tecnologias':['python','Django','HTML','CSS'],
        'tarefas': todas_as_tarefas,
        'exe' : execucao_as 
    }
    return render(request,'home.html',context)

def site(request):
    return HttpResponse("<h1>Nova pasta</h1>")

