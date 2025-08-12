from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from django.http import HttpResponseRedirect

from apps.notificacao.views import notificacao

from apps.user_admin.forms import cadastroAdminForms, perfilAdminForm, instituicaoForms, cursoForms, campusForms, categoriaForms, tipoForms, cadastroBibliotecarioForms, perfilBibliotecarioForms
from apps.user_admin.models import PerfilAdmin, Instituicao, Curso, Campus, Categoria, Tipos, PerfilBibliotecario

from apps.login_perfil.views import infor_perfis, deletar_obj, cadastrar_obj, editar_obj, editar_foto, redefinir_senha, deletar_foto_perfil, editar_user, senha_alt, envio_msg_rabbitmq
from apps.login_perfil.forms import senhaUsuarioForms

def verificar_auth_admin(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')
    
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permição para acessar essa página!')
        return redirect('home')

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: USER + PERFIL

# pagina inicial do perfil
@require_GET
def perfil_admin(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    return render(request, 'usuarios/admin/informacao/informacoes_admin.html', {'infor_admin':infor_admin})

# editar o proprio perfil do usuario
@require_http_methods(["GET", "POST"])
def editar_perfil_admin(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = editar_foto(request, PerfilAdmin, perfilAdminForm, 'Perfil alterado com sucesso!', 'editar_perfil_admin')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/admin/user/editar_perfil_adm.html', {'infor_admin': infor_admin, 'formulario': formulario})

# deletar a foto de perfil do usuario
@require_POST
def deletar_foto_admin(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_foto_perfil(request, id, PerfilAdmin, 'Foto de perfil deletada', 'Nenhuma foto!')

    return redirect('editar_perfil_admin')

# Função cadastrar novo user Admin e exibi-los
@require_http_methods(["GET", "POST"])
def cadastro_admin(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)
    
    if request.method == 'POST':
        formulario_cadastro_admin = cadastroAdminForms(request.POST)
        if formulario_cadastro_admin.is_valid():

            senha = senha_alt(request)

            usuario = formulario_cadastro_admin.save(commit=False)
            usuario.first_name = usuario.first_name.title()
            # set_password Criptografa e define a senha, nesse caso "0000"
            usuario.set_password("0000")
            # Permite acesso ao admin
            usuario.is_staff = True
            # Permite criar como superusuário
            usuario.is_superuser = True
            # Salva o Ususario
            usuario.save()

            envio_msg_rabbitmq(request, usuario.email, usuario.first_name, senha)
            
            notificacao_cad = notificacao(request, usuario, None, 'Bem vindo ao IF_Lib', f'  Olá {usuario.first_name}, seja muito bem vindo(a) ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!')

            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('cadastro_admin')

        # Exibe todos os erros de forma automatica        
        for field, errors in formulario_cadastro_admin.errors.items():
            for i in errors:
                messages.error(request, f'{field}: {i}')
        
    else:
        formulario_cadastro_admin = cadastroAdminForms()

    # dados da tabela de cadastro de admin
    # filtra somente os super usuarios ou seja os admins
    admin_tab = User.objects.filter(is_superuser=True).order_by('first_name')

    return render(request, 'usuarios/admin/user/cad_admin.html', {'formulario_cadastro_admin':formulario_cadastro_admin, 'admin_tab': admin_tab, 'infor_admin':infor_admin})

# deletar algum usuario admin
@require_POST
def deletar_user_admin(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, User, 'Admin deletado com sucesso!', id)

    return redirect('cadastro_admin')

# editar algum usuario admin
@require_http_methods(["GET", "POST"])
def editar_user_admin(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, User, cadastroAdminForms, 'ADMIN editado com sucesso!', 'cadastro_admin', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
    
    # Exibe todos os erros de forma automatica        
    for field, errors in formulario_edit.errors.items():
        for i in errors:
            messages.error(request, f'{field}: {i}')
        
    return render(request, 'usuarios/admin/user/editar_admin.html', {'formulario_edit_admin':formulario_edit, 'id':id, 'infor_admin':infor_admin})

# redefinir senha admin
@require_http_methods(["GET", "POST"])
def redefinir_senha_admin(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = redefinir_senha(request, senhaUsuarioForms, 'senha', 'confirmar_senha', 'As senhas não são iguais', 'Senha alterada com sucesso', 'Erro ao tentar alterar a senha:', 'redefinir_senha_admin')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/admin/user/redefinir_senha_admin.html', {'infor_admin':infor_admin, 'formulario':formulario})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: INSTITUIÇÃO

# cadastrar nova instituição
@require_http_methods(["GET", "POST"])
def cad_instituicao(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = cadastrar_obj(request, instituicaoForms, 'Instituição cadastrada com sucesso!', 'Erro ao cadastrar a instituição', 'cad_instituicao')
    
    if isinstance(formulario, HttpResponseRedirect):
        return formulario
    
    instituicao_tab = Instituicao.objects.all()

    return render(request, 'usuarios/admin/instituicao/instituições_admin.html', {'infor_admin':infor_admin, 'formulario':formulario, 'instituicao_tab':instituicao_tab})

# deletar instituição
@require_POST
def deletar_instituicao(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, Instituicao, 'Instituição deletada com sucesso!', id)
    return redirect('cad_instituicao')

# editar instituição
@require_http_methods(["GET", "POST"])
def editar_instituicao(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Instituicao, instituicaoForms, 'Instituição editada com sucesso!', 'cad_instituicao', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/instituicao/editar_instituicao.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: CURSO

# cadastrar novo curso
@require_http_methods(["GET", "POST"])
def cad_curso(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = cadastrar_obj(request, cursoForms, 'Curso cadastrado com sucesso!', 'Erro ao cadastrar o curso', 'cad_curso')
    
    if isinstance(formulario, HttpResponseRedirect):
        return formulario
    
    curso_tab = Curso.objects.all()

    return render(request, 'usuarios/admin/curso/cursos_admin.html', {'infor_admin':infor_admin, 'formulario':formulario, 'curso_tab':curso_tab})

# deletar curso
@require_POST
def deletar_curso(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, Curso, 'Curso deletado com sucesso!', id)
    return redirect('cad_curso')

# editar curso
@require_http_methods(["GET", "POST"])
def editar_curso(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Curso, cursoForms, 'Curso editado com sucesso!', 'cad_curso', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/curso/editar_curso.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: CAMPUS

# cadastrar novo campus
@require_http_methods(["GET", "POST"])
def cad_campus(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = cadastrar_obj(request, campusForms, 'Campus cadastrado com sucesso!', 'Erro ao cadastrar o campus', 'cad_campus')
    
    if isinstance(formulario, HttpResponseRedirect):
        return formulario
    
    campus_tab = Campus.objects.all()

    return render(request, 'usuarios/admin/campus/campus_admin.html', {'infor_admin':infor_admin, 'formulario':formulario, 'campus_tab':campus_tab})

# deletar campus
@require_POST
def deletar_campus(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, Campus, 'Campus deletado com sucesso!', id)
    return redirect('cad_campus')

# editar campus
@require_http_methods(["GET", "POST"])
def editar_campus(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Campus, campusForms, 'Campus editado com sucesso!', 'cad_campus', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/campus/editar_campus.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: CATEGORIAS

# cadastrar nova categoria
@require_http_methods(["GET", "POST"])
def cad_categoria(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = cadastrar_obj(request, categoriaForms, 'Categoria cadastrada com sucesso!', 'Erro ao cadastrar a categoria', 'cad_categoria')
    
    if isinstance(formulario, HttpResponseRedirect):
        return formulario
    
    categoria_tab = Categoria.objects.all()

    return render(request, 'usuarios/admin/categoria/categoria_admin.html', {'infor_admin':infor_admin, 'formulario':formulario, 'categoria_tab':categoria_tab})

# deletar categoria
@require_POST
def deletar_categoria(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, Categoria, 'Categoria deletada com sucesso!', id)
    return redirect('cad_categoria')

# editar categoria
@require_http_methods(["GET", "POST"])
def editar_categoria(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Categoria, categoriaForms, 'Categoria editada com sucesso!', 'cad_categoria', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/categoria/editar_categoria.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: TIPOS

# cadastrar novo tipo
@require_http_methods(["GET", "POST"])
def cad_tipo(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = cadastrar_obj(request, tipoForms, 'Tipo cadastrado com sucesso!', 'Erro ao cadastrar o Tipo', 'cad_tipo')
    
    if isinstance(formulario, HttpResponseRedirect):
        return formulario
    
    tipo_tab = Tipos.objects.all()

    return render(request, 'usuarios/admin/tipo/tipo_admin.html', {'infor_admin':infor_admin, 'formulario':formulario, 'tipo_tab':tipo_tab})

# deletar tipo
@require_POST
def deletar_tipo(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, Tipos, 'Tipo deletado com sucesso!', id)
    return redirect('cad_tipo')

# editar tipo
@require_http_methods(["GET", "POST"])
def editar_tipo(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Tipos, tipoForms, 'Tipo editado com sucesso!', 'cad_tipo', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/tipo/editar_tipo.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: BIBLIOTECARIOS

# cadastro de bibliotecario
@require_http_methods(["GET", "POST"])
def cad_bibliotecario(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)
    
    if request.method == 'POST':
        formulario_cadastro_bibliotecario = cadastroBibliotecarioForms(request.POST)
        formulario_perfil_bibliotecario = perfilBibliotecarioForms(request.POST)
        
        
        if formulario_cadastro_bibliotecario.is_valid() and formulario_perfil_bibliotecario.is_valid():

            senha = senha_alt(request)

            user_bibliotecario = formulario_cadastro_bibliotecario.save(commit=False)
            user_bibliotecario.first_name = user_bibliotecario.first_name.title()
            user_bibliotecario.set_password(str(senha))
            user_bibliotecario.save()

            perfil_bibliotecario = formulario_perfil_bibliotecario.save(commit=False)
            perfil_bibliotecario.usuario = user_bibliotecario
            perfil_bibliotecario.criador = request.user
            perfil_bibliotecario.instituicao = perfil_bibliotecario.campus.instituicao_campus
            perfil_bibliotecario.save()

            envio_msg_rabbitmq(request, user_bibliotecario.email, user_bibliotecario.first_name, senha)

            notificacao_cad = notificacao(request, user_bibliotecario, None, 'Bem vindo ao IF_Lib', f'  Olá {user_bibliotecario.first_name}, seja muito bem vindo(a) ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!')

            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('cad_bibliotecario')
            
        # Exibe todos os erros de forma automatica
        for field, errors in formulario_cadastro_bibliotecario.errors.items():
            for i in errors:
                messages.error(request, f'{field}: {i}')
        
    else:
        formulario_cadastro_bibliotecario = cadastroBibliotecarioForms()
        formulario_perfil_bibliotecario = perfilBibliotecarioForms()

    bibliotecario_tab = PerfilBibliotecario.objects.all().order_by('usuario__first_name')

    return render(request, 'usuarios/admin/bibliotecario/bibliotecario_admin.html', {'formulario_cadastro_bibliotecario':formulario_cadastro_bibliotecario, 'formulario_perfil_bibliotecario':formulario_perfil_bibliotecario, 'infor_admin':infor_admin, 'bibliotecario_tab':bibliotecario_tab})

# deletar bibliotecario
@require_POST
def deletar_bibliotecario(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    deletar_obj(request, User, 'Bibliotecário deletado com sucesso!', id)
    return redirect('cad_bibliotecario')

# editar algum usuario bibliotecario
@require_http_methods(["GET", "POST"])
def editar_user_bibliotecario(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_user(request, id, PerfilBibliotecario, cadastroBibliotecarioForms, perfilBibliotecarioForms, 'Bibliotecário editado com sucesso', 'cad_bibliotecario')
        
    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    formulario_edit_1, formulario_edit_2 = formulario_edit

    return render(request, 'usuarios/admin/bibliotecario/editar_bibliotecario.html', {'formulario_edit_1':formulario_edit_1, 'formulario_edit_2':formulario_edit_2, 'id':id, 'infor_admin':infor_admin})
