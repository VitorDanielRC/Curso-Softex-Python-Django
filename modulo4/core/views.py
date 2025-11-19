from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Tarefa
from .models import execucao
from .form import TarefaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def home(request):
 if request.method == 'POST':
    form = TarefaForm(request.POST)
 if form.is_valid():

    tarefa = form.save(commit=False)
 
    tarefa.user = request.user

    tarefa.save()
    return redirect('home')
 else:
    form = TarefaForm()

 todas_as_tarefas = Tarefa.objects.filter(user=request.user).order_by('criado_em')

 context = {
 'nome_usuario': request.user.username, 
 'tecnologias': ['Autenticação', 'ForeignKey', 'Login'],
 'tarefas': todas_as_tarefas,
 'form': form,
 }

 return render(request, 'home.html', context)



@login_required
def concluir_tarefa(request, pk):
 # 2. Modifique o 'get_object_or_404'
 # Busque a Tarefa pela 'pk' E ONDE o 'user' é o 'request.user'
    tarefa = get_object_or_404(Tarefa, pk=pk, user=request.user)
    if request.method == 'POST':
        tarefa.concluida = True
        tarefa.save() # Não se esqueça de salvar!
        return redirect('home')
    
@login_required
def deletar_tarefa(request, pk):
 # 3. Faça o mesmo filtro de segurança aqui
    tarefa = get_object_or_404(Tarefa, pk=pk, user=request.user)
    if request.method == 'POST':
        tarefa.delete()
        return redirect('home')

def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request,user)
        return redirect('home')
    else:
        form = UserCreationForm()
    context={'form':form}
    return render(request,'register.html', context)
        

