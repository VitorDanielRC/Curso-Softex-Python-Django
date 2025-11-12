from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tarefa
from .models import execucao
from .form import TarefaForm
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TarefaForm() # Cria um formulário vaz

    todas_as_tarefas = Tarefa.objects.all().order_by('-criada_em')
    execucao_as = execucao.objects.all()
    context={
        'nome_usuario':'Vitor',
        'tecnologias':['python','Django','HTML','CSS'],
        'tarefas': todas_as_tarefas,
        'exe' : execucao_as,
        'form':form
    }
    return render(request,'home.html',context)

def site(request):
    return HttpResponse("<h1>Nova pasta</h1>")

