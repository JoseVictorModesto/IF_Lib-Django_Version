from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages

from django.views.decorators.http import require_POST, require_GET, require_http_methods

from apps.login_perfil.views import infor_perfis, editar_user, editar_foto, deletar_foto_perfil, redefinir_senha
from apps.login_perfil.forms import senhaUsuarioForms

from apps.user_bibliotecario.models import PerfilProfessor

from apps.user_professor.forms import editarPerfilProfessorForms, editarUserProfessorForms, fotoProfessorForms

def verificar_auth(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acssar essa página!')
        return redirect('login')

    if not hasattr(request.user, 'usuario_professor') or request.user.usuario_professor.tipo_user != 'professor':
        messages.error(request, 'Você não tem permição para acessar essa página!')
        return redirect('home')

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES PROFESSOR: PERFIL
@require_GET
def perfil_professor(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth

    infor_professor = infor_perfis(request, PerfilProfessor)
    return render(request, 'usuarios/professor/user/perfil_professor.html', {'infor_professor':infor_professor})

@require_http_methods(["GET", "POST"])
def editar_perfil_professor(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_professor = infor_perfis(request, PerfilProfessor)
    id = infor_professor.id

    formulario_edit = editar_user(request, id, PerfilProfessor, editarUserProfessorForms, editarPerfilProfessorForms, 'Perfil editado com sucesso', 'editar_perfil_professor')

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
    
    formulario_edit_1, formulario_edit_2 = formulario_edit

    return render(request, 'usuarios/professor/user/editar_perfil_professor.html', {'infor_professor':infor_professor, 'formulario_edit_1':formulario_edit_1, 'formulario_edit_2':formulario_edit_2, 'id':id})

@require_http_methods(["GET", "POST"])
def editar_foto_professor(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_professor = infor_perfis(request, PerfilProfessor)

    formulario = editar_foto(request, PerfilProfessor, fotoProfessorForms, 'Perfil alterado com sucesso!', 'editar_foto_professor')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/professor/user/editar_foto_professor.html', {'infor_professor':infor_professor, 'formulario':formulario})

@require_POST
def deletar_foto_professor(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
        
    deletar_foto_perfil(request, id, PerfilProfessor, 'Foto de perfil deletada', 'Nenhuma foto!')

    return redirect('editar_foto_professor')

@require_http_methods(["GET", "POST"])
def redefinir_senha_professor(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth

    infor_professor = infor_perfis(request, PerfilProfessor)

    formulario = redefinir_senha(request, senhaUsuarioForms, 'senha', 'confirmar_senha', 'As senhas não são iguais', 'Senha alterada com sucesso', 'Erro ao tentar alterar a senha:', 'redefinir_senha_professor')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario 
    
    return render(request, 'usuarios/professor/user/redefinir_senha_professor.html', {'infor_professor': infor_professor, 'formulario':formulario})