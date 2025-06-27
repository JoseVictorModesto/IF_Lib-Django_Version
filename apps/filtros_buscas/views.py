from django.shortcuts import render, get_object_or_404
from apps.user_admin.models import Categoria, Tipos, Instituicao, Curso, Campus

def filtros(request, id, modelo_bd):
    filtro_id = get_object_or_404(modelo_bd, id=id)
    filtros = modelo_bd.objects.all()

    return filtro_id, filtros

def filtro_categoria(request, id):
    categoria_id, categorias = filtros(request, id, Categoria)
    return render(request, 'consultas/filtros/categoria.html', {'categoria_id':categoria_id, 'categorias':categorias})

def filtro_tipos(request, id):
    tipo_id, tipos = filtros(request, id, Tipos)
    return render(request, 'consultas/filtros/tipos.html', {'tipo_id':tipo_id, 'tipos':tipos})

def filtro_instituicao(request, id):
    instituicao_id, instituicoes = filtros(request, id, Instituicao)
    return render(request, 'consultas/filtros/instituicao.html', {'instituicao_id':instituicao_id, 'instituicoes':instituicoes})

def filtro_campus(request, id):
    campus_id, campus = filtros(request, id, Campus)
    return render(request, 'consultas/filtros/campus.html', {'campus_id':campus_id, 'campus':campus})

def filtro_cursos(request, id):
    curso_id, cursos = filtros(request, id, Curso)
    return render(request, 'consultas/filtros/curso.html', {'curso_id':curso_id, 'cursos':cursos})