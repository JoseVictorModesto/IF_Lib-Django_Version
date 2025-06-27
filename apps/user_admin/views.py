from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from apps.notificacao.models import Notificacao

from apps.user_admin.forms import cadastroAdminForms, perfilAdminForm, instituicaoForms, cursoForms, campusForms, categoriaForms, tipoForms, senhaAdminForms, cadastroBibliotecarioForms, perfilBibliotecarioForms
from apps.user_admin.models import PerfilAdmin, Instituicao, Curso, Campus, Categoria, Tipos, PerfilBibliotecario

from apps.login_perfil.views import infor_perfis, deletar_obj, cadastrar_obj, editar_obj, editar_foto, redefinir_senha, deletar_foto_perfil, editar_user

def verificar_auth_admin(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acssar essa página!')
        return redirect('login')
    
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permição para acessar essa página!')
        return redirect('home')

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: USER + PERFIL

# pagina inicial do perfil
def perfil_admin(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    return render(request, 'usuarios/admin/informacao/informacoes_admin.html', {'infor_admin':infor_admin})

# editar o proprio perfil do usuario
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
def deletar_foto_admin(request, id):
    deletar_foto_perfil(request, id, PerfilAdmin, 'Foto de perfil deletada', 'Nenhuma foto!')

    return redirect('editar_perfil_admin')

# Função cadastrar novo user Admin e exibi-los
def cadastro_admin(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)
    
    if request.method == 'POST':
        formulario_cadastro_admin = cadastroAdminForms(request.POST)
        if formulario_cadastro_admin.is_valid():
            usuario = formulario_cadastro_admin.save(commit=False)
            # set_password Criptografa e define a senha, nesse caso "0000"
            usuario.set_password("0000")
            # Permite acesso ao admin
            usuario.is_staff = True
            # Permite criar como superusuário
            usuario.is_superuser = True
            # Salva o Ususario
            usuario.save()

            notificao = Notificacao(
                remetente = request.user,
                destinatario = usuario,
                titulo_notificacao = 'Bem vindo ao IF_Lib',
                descricao_notificacao = 'Olá seja muito bem vindo ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!',
            )
            notificao.save()

            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('cadastro_admin')
        
        elif 'email' in formulario_cadastro_admin.errors:
            messages.error(request, 'E-mail inválido')

        else:
            messages.error(request, 'Erro ao editar usuário: Username já existe')
        
    else:
        formulario_cadastro_admin = cadastroAdminForms()

    # dados da tabela de cadastro de admin
    # filtra somente os super usuarios ou seja os admins
    admin_tab = User.objects.filter(is_superuser=True)

    return render(request, 'usuarios/admin/user/cad_admin.html', {'formulario_cadastro_admin':formulario_cadastro_admin, 'admin_tab': admin_tab, 'infor_admin':infor_admin})

# deletar algum usuario admin
def deletar_user_admin(request, id):
    deletar_obj(request, User, 'Admin deletado com sucesso!', id)

    return redirect('cadastro_admin')

# editar algum usuario admin
def editar_user_admin(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, User, cadastroAdminForms, 'ADMIN editado com sucesso!', 'cadastro_admin', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
    
    elif 'email' in formulario_edit.errors:
            messages.error(request, 'E-mail inválido')

    else:
        messages.error(request, 'Erro ao editar usuário: Username já existe')
        
    return render(request, 'usuarios/admin/user/editar_admin.html', {'formulario_edit_admin':formulario_edit, 'id':id, 'infor_admin':infor_admin})

# redefinir senha admin
def redefinir_senha_admin(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = redefinir_senha(request, senhaAdminForms, 'senha', 'confirmar_senha', 'As senhas não são iguais', 'Senha alterada com sucesso', 'Erro ao tentar alterar a senha:', 'redefinir_senha_admin')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/admin/user/redefinir_senha_admin.html', {'infor_admin':infor_admin, 'formulario':formulario})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: INSTITUIÇÃO

# cadastrar nova instituição
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
def deletar_instituicao(request, id):
    deletar_obj(request, Instituicao, 'Instituição deletada com sucesso!', id)
    return redirect('cad_instituicao')

# editar instituição
def editar_instituicao(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Instituicao, instituicaoForms, 'Intituição editada com sucesso!', 'cad_instituicao', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/instituicao/editar_instituicao.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: CURSO

# cadastrar novo curso
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
def deletar_curso(request, id):
    deletar_obj(request, Curso, 'Curso deletado com sucesso!', id)
    return redirect('cad_curso')

# editar curso
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
def deletar_campus(request, id):
    deletar_obj(request, Campus, 'Campus deletado com sucesso!', id)
    return redirect('cad_campus')

# editar campus
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
def cad_categoria(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = cadastrar_obj(request, categoriaForms, 'Categoria cadastrada com sucesso!', 'Erro ao cadastrar a categoria', 'cad_categoria')
    
    if isinstance(formulario, HttpResponseRedirect):
        return formulario
    
    categoria_tab = Categoria.objects.all()

    return render(request, 'usuarios/admin/categoria/categoria_admin.htm', {'infor_admin':infor_admin, 'formulario':formulario, 'categoria_tab':categoria_tab})

# deletar categoria
def deletar_categoria(request, id):
    deletar_obj(request, Categoria, 'Categoria deletada com sucesso!', id)
    return redirect('cad_categoria')

# editar categoria
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
def deletar_tipo(request, id):
    deletar_obj(request, Tipos, 'Tipo deletado com sucesso!', id)
    return redirect('cad_tipo')

# editar tipo
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
def cad_bibliotecario(request):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)
    
    if request.method == 'POST':
        formulario_cadastro_bibliotecario = cadastroBibliotecarioForms(request.POST)
        formulario_perfil_bibliotecario = perfilBibliotecarioForms(request.POST)
        
        
        if formulario_cadastro_bibliotecario.is_valid() and formulario_perfil_bibliotecario.is_valid():
            print("Formulários válidos")
            user_bibliotecario = formulario_cadastro_bibliotecario.save(commit=False)
            user_bibliotecario.set_password("0000")
            user_bibliotecario.save()

            perfil_bibliotecario = formulario_perfil_bibliotecario.save(commit=False)
            perfil_bibliotecario.usuario = user_bibliotecario
            perfil_bibliotecario.criador = request.user
            perfil_bibliotecario.instituicao = perfil_bibliotecario.campus.instituicao_campus
            perfil_bibliotecario.save()

            notificao = Notificacao(
                remetente = request.user,
                destinatario = user_bibliotecario,
                titulo_notificacao = 'Bem vindo ao IF_Lib',
                descricao_notificacao = 'Olá seja muito bem vindo ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!',
            )
            notificao.save()

            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('cad_bibliotecario')
            
        elif 'email' in formulario_cadastro_bibliotecario.errors:
            messages.error(request, 'E-mail inválido')

        else:
            messages.error(request, 'Erro ao cadastrar usuário: Username já existe')
        
    else:
        formulario_cadastro_bibliotecario = cadastroBibliotecarioForms()
        formulario_perfil_bibliotecario = perfilBibliotecarioForms()

    bibliotecario_tab = PerfilBibliotecario.objects.all()

    return render(request, 'usuarios/admin/bibliotecario/bibliotecario_admin.html', {'formulario_cadastro_bibliotecario':formulario_cadastro_bibliotecario, 'formulario_perfil_bibliotecario':formulario_perfil_bibliotecario, 'infor_admin':infor_admin, 'bibliotecario_tab':bibliotecario_tab})

# deletar bibliotecario
def deletar_bibliotecario(request, id):
    deletar_obj(request, User, 'Bibliotecário deletado com sucesso!', id)
    return redirect('cad_bibliotecario')

# editar algum usuario bibliotecario
def editar_user_bibliotecario(request, id):
    usuario_auth = verificar_auth_admin(request)
    if usuario_auth:
        return usuario_auth
    
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_user(request, id, PerfilBibliotecario, cadastroBibliotecarioForms, perfilBibliotecarioForms, 'Bibliotecario editado com sucesso', 'cad_bibliotecario')
        
    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    formulario_edit_1, formulario_edit_2 = formulario_edit

    return render(request, 'usuarios/admin/bibliotecario/editar_biblioteacrio.html', {'formulario_edit_1':formulario_edit_1, 'formulario_edit_2':formulario_edit_2, 'id':id, 'infor_admin':infor_admin})
