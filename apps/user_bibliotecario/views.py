from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from apps.user_admin.models import PerfilBibliotecario
from apps.user_bibliotecario.models import PerfilProfessor, PerfilAluno

from apps.notificacao.views import notificacao

from apps.user_bibliotecario.forms import fotoBibliotecarioForms, editarBibliotecarioForms
from apps.user_bibliotecario.forms import cadastroProfessorForm, cadastroAlunoForm, perfilProfessorForm, perfilAlunoForm, editarProfessorForm, editarAlunoForm

from apps.login_perfil.views import infor_perfis, deletar_obj, editar_user
from apps.login_perfil.views import editar_foto, deletar_foto_perfil, redefinir_senha, editar_obj
from apps.login_perfil.forms import senhaUsuarioForms

from apps.conteudos.models import ConteudoAcademico

def verificar_auth(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')

    if not hasattr(request.user, 'usuario_bibliotecario') or request.user.usuario_bibliotecario.tipo_user != 'bibliotecario':
        messages.error(request, 'Você não tem permição para acessar essa página!')
        return redirect('home')
    
# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES BIBLIOTECARIO: PERFIL
@require_GET
def informacoes_bibliotecario(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)

    return render(request, 'usuarios/bibliotecarios/informacao/informacoes_bibliotecario.html', {'infor_bibliotecario':infor_bibliotecario})

@require_http_methods(["GET", "POST"])
def editar_perfil_bibliotecario(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)
    id = infor_bibliotecario.usuario.id

    formulario_edit = editar_obj(request, User, editarBibliotecarioForms, 'Perfil editado com sucesso!', 'informacoes_bibliotecario', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
    
    elif 'email' in formulario_edit.errors:
            messages.error(request, 'E-mail inválido')

    return render(request, 'usuarios/bibliotecarios/user/editar_perfil_biblioitecario.html', {'infor_bibliotecario':infor_bibliotecario, 'id':id, 'formulario_edit':formulario_edit})

@require_http_methods(["GET", "POST"])
def editar_foto_bibliotecario(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)

    formulario = editar_foto(request, PerfilBibliotecario, fotoBibliotecarioForms, 'Perfil alterado com sucesso!', 'editar_foto_bibliotecario')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/bibliotecarios/user/editar_foto_bibliotecario.html', {'infor_bibliotecario': infor_bibliotecario, 'formulario': formulario})

@require_POST
def deletar_foto_bibliotecario(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_foto_perfil(request, id, PerfilBibliotecario, 'Foto de perfil deletada', 'Nenhuma foto!')

    return redirect('editar_foto_bibliotecario')

@require_http_methods(["GET", "POST"])
def redefinir_senha_bibliotecario(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)

    formulario = redefinir_senha(request, senhaUsuarioForms, 'senha', 'confirmar_senha', 'As senhas não são iguais', 'Senha alterada com sucesso', 'Erro ao tentar alterar a senha:', 'redefinir_senha_bibliotecario')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario   

    return render(request, 'usuarios/bibliotecarios/user/redefinir_senha_bibliotecario.html', {'infor_bibliotecario': infor_bibliotecario, 'formulario':formulario})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES BIBLIOTECARIO: PROFESSOR

@require_http_methods(["GET", "POST"])
def cad_professor(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)

    if request.method == 'POST':
        formulario_cadastro_professor = cadastroProfessorForm(request.POST)
        formulario_perfil_professor = perfilProfessorForm(request.POST)

        if formulario_cadastro_professor.is_valid() and formulario_perfil_professor.is_valid():

            user_professor = formulario_cadastro_professor.save(commit=False)
            user_professor.first_name = user_professor.first_name.title()
            user_professor.set_password('0000')
            user_professor.save()

            perfil_professor = formulario_perfil_professor.save(commit=False)
            perfil_professor.usuario = user_professor
            perfil_professor.criador = request.user
            perfil_professor.campus = request.user.usuario_bibliotecario.campus
            perfil_professor.instituicao = perfil_professor.campus.instituicao_campus
            perfil_professor.save()

            notificacao_cad = notificacao(request, user_professor, None, 'Bem vindo ao IF_Lib', f'  Olá {user_professor.first_name}, seja muito bem vindo(a) ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!')

            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('cad_professor')
            
        elif 'email' in formulario_cadastro_professor.errors:
            messages.error(request, 'Erro ao cadastrar usuário: E-mail inválido')

        else:
            messages.error(request, 'Erro ao cadastrar usuário: Username já existe')

    else:
        formulario_cadastro_professor = cadastroProfessorForm()
        formulario_perfil_professor = perfilProfessorForm()
                                                                                                    # usar o __ para acessar um atributo ligado a uma chave extrangeira
                                                                                                    # ou seja “atributo dentro de outro atributo” como nesse caso 'usuario' dentro de User
                                                                                                    # que esta ligado a tabela User e o atributo first_name
    professor_tab = PerfilProfessor.objects.filter(campus = request.user.usuario_bibliotecario.campus).order_by('usuario__first_name')

    return render(request, 'usuarios/bibliotecarios/professores/cad_professor.html', {'formulario_cadastro_professor':formulario_cadastro_professor, 'formulario_perfil_professor':formulario_perfil_professor, 'infor_bibliotecario':infor_bibliotecario, 'professor_tab':professor_tab})

@require_POST
def deletar_professor(request, id):
    deletar_obj(request, User, 'Professor deletado com sucesso!', id)
    return redirect('cad_professor')

@require_http_methods(["GET", "POST"])
def editar_professor(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)

    formulario_edit = editar_user(request, id, PerfilProfessor, cadastroProfessorForm, editarProfessorForm, 'Professor editado com sucesso', 'cad_professor')

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
    
    formulario_edit_1, formulario_edit_2 = formulario_edit

    return render(request, 'usuarios/bibliotecarios/professores/editar_professor.html', {'infor_bibliotecario':infor_bibliotecario, 'formulario_edit_1':formulario_edit_1, 'formulario_edit_2':formulario_edit_2, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES BIBLIOTECARIO: ALUNO

@require_http_methods(["GET", "POST"])
def cad_aluno(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)
    
    if request.method == 'POST':
        formulario_cadastro_aluno = cadastroAlunoForm(request.POST)
        formulario_perfil_aluno = perfilAlunoForm(request.POST)

        if formulario_cadastro_aluno.is_valid() and formulario_perfil_aluno.is_valid():
            user_aluno = formulario_cadastro_aluno.save(commit=False)
            user_aluno.first_name = user_aluno.first_name.title()
            user_aluno.set_password('0000')
            user_aluno.save()

            perfil_aluno = formulario_perfil_aluno.save(commit=False)
            perfil_aluno.usuario = user_aluno
            perfil_aluno.criador = request.user
            perfil_aluno.campus = request.user.usuario_bibliotecario.campus
            perfil_aluno.instituicao = perfil_aluno.campus.instituicao_campus
            perfil_aluno.save()

            notificacao_cad = notificacao(request, user_aluno, None, 'Bem vindo ao IF_Lib', f'  Olá {user_aluno.first_name}, seja muito bem vindo(a) ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!')
            
            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('cad_aluno')
            
        elif 'email' in formulario_cadastro_aluno.errors:
            messages.error(request, 'Erro ao cadastrar usuário: E-mail inválido')

        else:
            messages.error(request, 'Erro ao cadastrar usuário: Username já existe')

    else:
        formulario_cadastro_aluno = cadastroAlunoForm()
        formulario_perfil_aluno = perfilAlunoForm()

    aluno_tab = PerfilAluno.objects.filter(campus = request.user.usuario_bibliotecario.campus).order_by('usuario__first_name')

    return render(request, 'usuarios/bibliotecarios/alunos/cad_aluno.html', {'infor_bibliotecario':infor_bibliotecario, 'formulario_cadastro_aluno':formulario_cadastro_aluno, 'formulario_perfil_aluno':formulario_perfil_aluno, 'aluno_tab':aluno_tab})

@require_POST
def deletar_aluno(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, User, 'Aluno deletado com sucesso!', id)
    return redirect('cad_aluno')

@require_http_methods(["GET", "POST"])
def editar_aluno(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)

    formulario_edit = editar_user(request, id, PerfilAluno, cadastroAlunoForm, editarAlunoForm, 'Aluno editado com sucesso', 'cad_aluno')

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
    
    formulario_edit_1, formulario_edit_2 = formulario_edit

    return render(request, 'usuarios/bibliotecarios/alunos/editar_aluno.html', {'infor_bibliotecario':infor_bibliotecario, 'formulario_edit_1':formulario_edit_1, 'formulario_edit_2':formulario_edit_2, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES BIBLIOTECARIO: CAI

# exibir a tabela de conteudos academicos
@require_GET
def conteudos_cai_bibliotecario(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth

    infor_bibliotecario = infor_perfis(request, PerfilBibliotecario)

    conteudo_cai_tab = ConteudoAcademico.objects.filter(campus_conteudo = request.user.usuario_bibliotecario.campus).order_by('-data_envio')

    return render(request, 'usuarios/bibliotecarios/conteudos/conteudo_cai_bibliotecario.html', {'infor_bibliotecario':infor_bibliotecario, 'conteudo_cai_tab':conteudo_cai_tab})

# deletar conteudo
def deleta_cai_bibliotecario(request, id):
    deletar_obj(request,ConteudoAcademico, 'Conteudo deletado com sucesso!', id )
    return redirect('conteudos_cai_bibliotecario')

