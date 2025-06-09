from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from apps.user_admin.forms import cadastroAdminForms, perfilAdminForm, instituicaoForms, cursoForms, campusForms, categoriaForms, tipoForms, senhaAdminForms
from apps.user_admin.models import PerfilAdmin, Instituicao, Curso, Campus, Categoria, Tipos

from apps.login_perfil.views import infor_perfis, deletar_obj, cadastrar_obj, editar_obj, editar_foto, redefinir_senha

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: USER + PERFIL

# pagina inicial do perfil
def perfil_admin(request):
    infor_admin = infor_perfis(request, PerfilAdmin)

    return render(request, 'usuarios/admin/informacao/informacoes_admin.html', {'infor_admin':infor_admin})

# editar o proprio perfil do usuario
def editar_perfil_admin(request):
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = editar_foto(request, PerfilAdmin, perfilAdminForm, 'Perfil alterado com sucesso!', 'editar_perfil_admin')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/admin/user/editar_perfil_adm.html', {'infor_admin': infor_admin, 'formulario': formulario})

# deletar a foto de perfil do usuario
def deletar_foto_perfil(request, id):
    # procura um perfil pelo id a partir do model PerfilAdmin e que esteja logado ou 404
    perfil = get_object_or_404(PerfilAdmin, id=id, usuario=request.user)
    
    # se o perfil tiver foto
    if perfil.foto_perfil:
        # sera deletado e salvo as alterações
        perfil.foto_perfil.delete()
        perfil.save()
        messages.success(request, 'Foto de perfil alterada')

    else:
        messages.error(request, 'Nenhuma foto!')

    return redirect('editar_perfil_admin')

# Função cadastrar novo user Admin e exibi-los
def cadastro_admin(request):
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
            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('cadastro_admin')
        
        else:
            print(formulario_cadastro_admin.errors)
            messages.error(request, 'Erro ao cadastrar usuário: Username já existe')
        
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
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, User, cadastroAdminForms, 'ADMIN editado com sucesso!', 'cadastro_admin', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit
        
    return render(request, 'usuarios/admin/user/editar_admin.html', {'formulario_edit_admin':formulario_edit, 'id':id, 'infor_admin':infor_admin})

# redefinir senha admin
def redefinir_senha_admin(request):
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = redefinir_senha(request, senhaAdminForms, 'senha', 'confirmar_senha', 'As senhas não são iguais', 'Senha alterada com sucesso', 'Erro ao tentar alterar a senha:', 'redefinir_senha_admin')

    if isinstance(formulario, HttpResponseRedirect):
        return formulario

    return render(request, 'usuarios/admin/user/redefinir_senha_admin.html', {'infor_admin':infor_admin, 'formulario':formulario})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: INSTITUIÇÃO

# cadastrar nova instituição
def cad_instituicao(request):
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
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Instituicao, instituicaoForms, 'Intituição editada com sucesso!', 'cad_instituicao', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/instituicao/editar_instituicao.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})


# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: CURSOS

# cadastrar novo curso
def cad_curso(request):
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
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Curso, cursoForms, 'Curso editado com sucesso!', 'cad_curso', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/curso/editar_curso.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: CAMPUS

# cadastrar novo campus
def cad_campus(request):
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
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Campus, campusForms, 'Campus editado com sucesso!', 'cad_campus', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/campus/editar_campus.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: CATEGORIAS

# cadastrar nova categoria
def cad_categoria(request):
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario = cadastrar_obj(request, categoriaForms, 'Categoria cadastrada com sucesso!', 'Erro ao cadastrar a categoria', 'cad_categoria')
    
    if isinstance(formulario, HttpResponseRedirect):
        return formulario
    
    categoria_tab = Categoria.objects.all()

    return render(request, 'usuarios/admin/categoria/categoria_admin.htm', {'infor_admin':infor_admin, 'formulario':formulario, 'categoria_tab':categoria_tab})

# deletar categoria
def deletar_categoria(request, id):
    deletar_obj(request, Categoria, 'Categoria deletado com sucesso!', id)
    return redirect('cad_categoria')

# editar categoria
def editar_categoria(request, id):
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Categoria, categoriaForms, 'Categoria editada com sucesso!', 'cad_categoria', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/categoria/editar_categoria.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: TIPOS

# cadastrar novo tipo
def cad_tipo(request):
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
    infor_admin = infor_perfis(request, PerfilAdmin)

    formulario_edit = editar_obj(request, Tipos, tipoForms, 'Tipo editado com sucesso!', 'cad_tipo', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'usuarios/admin/tipo/editar_tipo.html', {'infor_admin':infor_admin, 'formulario_edit':formulario_edit, 'id':id})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ADMIN: BIBLIOTECARIOS
