from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages

from django.views.decorators.http import require_GET, require_http_methods, require_POST

from apps.login_perfil.views import infor_perfis, editar_user, editar_foto, deletar_foto_perfil, redefinir_senha
from apps.login_perfil.forms import senhaUsuarioForms

from apps.user_bibliotecario.models import PerfilAluno

from apps.user_aluno.forms import editarPerfilAlunoForms, editarUserAluno, fotoAlunoForms

from apps.conteudos.models import ConteudoAcademico, CaixaFavoritos, CaixaFavoritosExternos

def verificar_auth(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')

    if not hasattr(request.user, 'usuario_aluno') or request.user.usuario_aluno.tipo_user != 'aluno':
        messages.error(request, 'Você não tem permição para acessar essa página!')
        return redirect('home')

# --------------------------------------------------------------------------------------------------------------------------

@require_GET
def perfil_aluno(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_aluno = infor_perfis(request, PerfilAluno)

    conteudo_aluno = ConteudoAcademico.objects.filter(conteudo_autores__autor = request.user).order_by('-id')

    try:
        caixa_favoritos_aluno = CaixaFavoritos.objects.get(usuario=request.user)
        favoritos = caixa_favoritos_aluno.conteudo_cai.all().order_by('titulo')

    except CaixaFavoritos.DoesNotExist:
        favoritos = []

    try:
        caixa_favoritos_professor = CaixaFavoritosExternos.objects.get(usuario=request.user)
        favoritos_ex = caixa_favoritos_professor.conteudo_ce.all().order_by('titulo')

    except CaixaFavoritosExternos.DoesNotExist:
        favoritos_ex = []

    return render(request, 'usuarios/aluno/user/perfil_aluno.html', {'infor_aluno':infor_aluno, 'conteudo_aluno':conteudo_aluno, 'favoritos':favoritos, 'favoritos_ex':favoritos_ex})

@require_http_methods(['GET', 'POST'])
def editar_perfil_aluno(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_aluno = infor_perfis(request, PerfilAluno)
    id = infor_aluno.id

    formulario_edit = editar_user(request, id, PerfilAluno, editarUserAluno, editarPerfilAlunoForms, 'Perfil editado com sucesso', 'editar_perfil_aluno')

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
    
    formulario_edit_1, formulario_edit_2 = formulario_edit

    return render(request, 'usuarios/aluno/user/editar_perfil_aluno.html', {'infor_aluno':infor_aluno, 'formulario_edit_1':formulario_edit_1, 'formulario_edit_2':formulario_edit_2, 'id':id})

@require_http_methods(['GET', 'POST'])
def editar_foto_aluno(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_aluno = infor_perfis(request, PerfilAluno)

    formulario = editar_foto(request, PerfilAluno, fotoAlunoForms, 'Perfil alterado com sucesso!', 'editar_foto_aluno')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/aluno/user/editar_foto_aluno.html', {'infor_aluno':infor_aluno, 'formulario':formulario})   

@require_POST
def deletar_foto_aluno(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_foto_perfil(request, id, PerfilAluno, 'Foto de perfil deletada', 'Nenhuma foto!')

    return redirect('editar_foto_aluno')

@require_http_methods(['GET', 'POST'])
def redefinir_senha_aluno(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_aluno = infor_perfis(request, PerfilAluno)

    formulario = redefinir_senha(request, senhaUsuarioForms, 'senha', 'confirmar_senha', 'As senhas não são iguais', 'Senha alterada com sucesso', 'Erro ao tentar alterar a senha:', 'redefinir_senha_aluno')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario 
    
    return render(request, 'usuarios/aluno/user/redefinir_senha_aluno.html', {'infor_aluno': infor_aluno, 'formulario':formulario})  

# --------------------------------------------------------------------------------------------------------------------------

@require_GET
def caixa_conteudos_alunos(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth

    conteudo_cai_nao_validado = ConteudoAcademico.objects.filter(conteudo_autores__autor = request.user, validado=False).order_by('-id')
    conteudo_cai_validado = ConteudoAcademico.objects.filter(conteudo_autores__autor = request.user, validado=True).order_by('-id')

    return render(request, 'usuarios/aluno/caixas/caixa_conteudos_aluno.html', {'conteudo_cai_nao_validado':conteudo_cai_nao_validado,
                                                                                'conteudo_cai_validado':conteudo_cai_validado,})