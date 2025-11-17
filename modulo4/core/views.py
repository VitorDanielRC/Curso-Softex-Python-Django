from django.shortcuts import render, redirect, get_object_or_404
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

    todas_as_tarefas = Tarefa.objects.all().order_by('criada_em')
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

def concluir_tarefa(request, pk):
# 1. Busca a tarefa pela 'pk' (ID) vinda da URL.
# Se não achar, retorna um erro 404.
    tarefa = get_object_or_404(Tarefa, pk=pk)
# 2. Segurança: Apenas execute se o método for POST
    if request.method == 'POST':
# 3. A Lógica de "Update"
        tarefa.concluida = True
        tarefa.save() # Não se esqueça de salvar!
# 4. Redireciona de volta para a 'home' (Padrão PRG)
    return redirect('home')
def deletar_tarefa(request, pk):
# 1. Busca a tarefa
    tarefa = get_object_or_404(Tarefa, pk=pk)
# 2. Segurança: Apenas execute se o método for POST
    if request.method == 'POST':
# 3. A Lógica de "Delete"
        tarefa.delete()
# 4. Redireciona de volta para a 'home'
    return redirect('home')
