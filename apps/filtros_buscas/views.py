from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_GET
 
from apps.user_admin.models import Categoria, Tipos, Instituicao, Curso, Campus

def filtros(request, id, modelo_bd, filtro):
    filtro_obj = get_object_or_404(modelo_bd, id=id)
    filtro_itens = modelo_bd.objects.order_by(filtro)

    return filtro_obj, filtro_itens

@require_GET
def filtro_categoria(request, id):
    categoria_id, categorias = filtros(request, id, Categoria, 'nome_categoria')
    return render(request, 'consultas/filtros/categoria.html', {'categoria_id':categoria_id, 'categorias':categorias})

@require_GET
def filtro_tipos(request, id):
    tipo_id, tipos = filtros(request, id, Tipos, 'nome_tipo')
    return render(request, 'consultas/filtros/tipos.html', {'tipo_id':tipo_id, 'tipos':tipos})

@require_GET
def filtro_instituicao(request, id):
    instituicao_id, instituicoes = filtros(request, id, Instituicao, 'nome_instituicao')
    return render(request, 'consultas/filtros/instituicao.html', {'instituicao_id':instituicao_id, 'instituicoes':instituicoes})

@require_GET
def filtro_campus(request, id):
    campus_id, campus = filtros(request, id, Campus, 'nome_campus')
    return render(request, 'consultas/filtros/campus.html', {'campus_id':campus_id, 'campus':campus})

@require_GET
def filtro_cursos(request, id):
    curso_id, cursos = filtros(request, id, Curso, 'nome_curso')
    return render(request, 'consultas/filtros/curso.html', {'curso_id':curso_id, 'cursos':cursos})