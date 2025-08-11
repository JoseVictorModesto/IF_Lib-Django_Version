from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from django.views.decorators.http import require_GET
 
from apps.user_admin.models import Categoria, Tipos, Instituicao, Curso, Campus

from apps.conteudos.models import ConteudoAcademico, ConteudoExterno

def filtros(request, id, modelo_bd, filtro):
    filtro_obj = get_object_or_404(modelo_bd, id=id)
    filtro_itens = modelo_bd.objects.order_by(filtro)

    return filtro_obj, filtro_itens

def obj_filtro(request, modelo, atr_obj, obj_id):
    ordenados_por = request.GET.get('ordenados_por', '-qtd_favoritos')
    filtro_dici = {
        'validado': True,
        f'{atr_obj}': obj_id
    }
    conteudo_cai = modelo.objects.filter(**filtro_dici).order_by(ordenados_por)

    conteudo_paginator = Paginator(conteudo_cai, 6)
    page_num = request.GET.get('page')
    page = conteudo_paginator.get_page(page_num)

    return ordenados_por, page

@require_GET
def filtro_categoria(request, id):
    categoria_id, categorias = filtros(request, id, Categoria, 'nome_categoria')
    ordenados_por, page = obj_filtro(request, ConteudoAcademico, 'categoria_conteudo', categoria_id)

    return render(request, 'consultas/filtros/categoria.html', {'categoria_id':categoria_id, 'categorias':categorias, 'ordenados_por':ordenados_por, 'page':page})

@require_GET
def filtro_tipos(request, id):
    tipo_id, tipos = filtros(request, id, Tipos, 'nome_tipo')
    ordenados_por, page = obj_filtro(request, ConteudoAcademico, 'tipos_conteudo', tipo_id)

    return render(request, 'consultas/filtros/tipos.html', {'tipo_id':tipo_id, 'tipos':tipos, 'ordenados_por':ordenados_por, 'page':page})

@require_GET
def filtro_instituicao(request, id):
    instituicao_id, instituicoes = filtros(request, id, Instituicao, 'nome_instituicao')
    ordenados_por, page = obj_filtro(request, ConteudoAcademico, 'instituicao_conteudo', instituicao_id)

    return render(request, 'consultas/filtros/instituicao.html', {'instituicao_id':instituicao_id, 'instituicoes':instituicoes, 'ordenados_por':ordenados_por, 'page':page})

@require_GET
def filtro_campus(request, id):
    campus_id, campus = filtros(request, id, Campus, 'nome_campus')
    ordenados_por, page = obj_filtro(request, ConteudoAcademico, 'campus_conteudo', campus_id)

    return render(request, 'consultas/filtros/campus.html', {'campus_id':campus_id, 'campus':campus, 'ordenados_por':ordenados_por, 'page':page})

@require_GET
def filtro_cursos(request, id):
    curso_id, cursos = filtros(request, id, Curso, 'nome_curso')
    ordenados_por, page = obj_filtro(request, ConteudoAcademico, 'curso_conteudo', curso_id)

    return render(request, 'consultas/filtros/curso.html', {'curso_id':curso_id, 'cursos':cursos, 'page':page, 'ordenados_por':ordenados_por})

@require_GET
def filtro_externos(request):
    ordenados_por = request.GET.get('ordenados_por', '-qtd_favoritos')

    conteudo_ce = ConteudoExterno.objects.all().order_by(ordenados_por)

    conteudo_paginator = Paginator(conteudo_ce, 6)
    page_num = request.GET.get('page')
    page = conteudo_paginator.get_page(page_num)

    return render(request, 'consultas/filtros/conteudos_externos.html', {'page':page, 'ordenados_por':ordenados_por})

@require_GET
def busca_principal(request):

    ordenados_por = request.GET.get('ordenados_por', '-qtd_favoritos')
    palavra_chave = request.GET.get('busca_principal_name', '')

    conteudo_cai = ConteudoAcademico.objects.filter(validado=True).order_by(ordenados_por)
    conteudo_ce = ConteudoExterno.objects.all().order_by(ordenados_por)

    if not palavra_chave:
        conteudo_cai = []
        conteudo_ce = []

    elif palavra_chave:
        conteudo_cai = conteudo_cai.filter(titulo__icontains=palavra_chave)
        conteudo_ce = conteudo_ce.filter(titulo__icontains=palavra_chave)
            
    return render(request, 'consultas/pesquisas/busca_principal.html', {'conteudo_cai':conteudo_cai, 'conteudo_ce':conteudo_ce, 'palavra_chave':palavra_chave, 'ordenados_por':ordenados_por})
