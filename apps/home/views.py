from django.shortcuts import render
from apps.user_admin.models import Categoria

from apps.conteudos.models import ConteudoAcademico

# Função exibição do index
def index(request):
    categorias = Categoria.objects.all().order_by('nome_categoria')
    
    categorias_com_conteudos = []
    for i in categorias:
        conteudos = ConteudoAcademico.objects.filter(categoria_conteudo=i, validado=True).order_by('-id')
        categorias_com_conteudos.append((i, conteudos))
    
    context = {
        'categorias_com_conteudos': categorias_com_conteudos,
    }
    
    return render(request, 'main/index.html', context)
