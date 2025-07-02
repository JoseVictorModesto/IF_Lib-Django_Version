from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import auth
from django.contrib.auth import update_session_auth_hash

from apps.login_perfil.forms import LoginForms

from django.contrib import messages

from django.views.decorators.http import require_POST

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES LOGIN + LOGOUT

# Função de exibir e efetuar login
def login(request):
    formulario_login = LoginForms()

    # se a requisição do formulario de cadastro for post crie 
    # uma instância do formulário LoginForms com os dados enviados pelo usuário.
    if request.method == 'POST':
        formulario_login = LoginForms(request.POST)

        # verifica se o formulario e valido
        if formulario_login.is_valid():
            matricula=formulario_login['matricula_login'].value()
            senha=formulario_login['senha_login'].value()

        # serve para autenticar o login do usuario com base nos dados fornecidos
        # verifica se a matricula e a senha fornecidos correspondem a um usuário existente no banco de dados
        usuario = auth.authenticate(
            request,
            username = matricula,
            password = senha
        )

        # verifica se o "usuario não é none" ou seja se ele existe no bd e 
        # se o usuário foi autenticado com sucesso, a matrícula e a senha estão corretas
        if usuario is not None:

            # se sim, Realiza o login do usuário, e cria uma sessão válida para ele.
            auth.login(request, usuario)

            # mensagem de sucesso
            messages.success(request, f'Seja bem vindo {request.user.first_name} ao Lib')         
            return redirect('home')
        
        # caso contrario retorna uma mensagem de erro e redireciona para pag de login
        else:
            # mensagem de erro
            messages.error(request, f'Erro Login, matícula ou senha incorretos!')
            return redirect('login')
        
    # renderiza pagina de login
    return render(request, 'login/login.html', {'formulario_login':formulario_login})

# logout usuario
@require_POST
def logout(request):
    # logout (sair) da sessão de login
    auth.logout(request)

    #mensagem sucesso
    messages.success(request, f'Logout efetuado!')

    return redirect('home')

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES GLOBAIS

# funçao global de informlções basicas dos perfis
def infor_perfis(request, modelo_perfil):
    # puxa as informações do usuario a partir do model PerfilAdmin que esteja logado
    # caso o usuario recem criado nao tenha ainda uma tabela no bd o django cria uma para esse user
    perfil, perfil_creat = modelo_perfil.objects.get_or_create(usuario=request.user)
    return perfil

# funçao global de deletar objetos
def deletar_obj(request, modelo, mensagem, id):
    # puxa e guarda um objeto pelo id de dentro do modelo repassado ou retorna um erro 404
    objeto = get_object_or_404(modelo, id=id)
    # deleta esse objeto do banco de dados
    objeto.delete()

    messages.success(request, mensagem)

# funçao global de cadastrar objetos
def cadastrar_obj(request, modelo_formulario, mensagem_1, mensagem_2, retorno_pag):
    if request.method == 'POST':
        formulario = modelo_formulario(request.POST)
        if formulario.is_valid():
            objeto = formulario.save(commit=False)
            objeto.criador = request.user
            objeto.save()
            formulario.save_m2m()
            messages.success(request, mensagem_1)
            return redirect(retorno_pag)
        
        else:
            messages.error(request, mensagem_2)

    else:
        formulario = modelo_formulario()

    return formulario

# funçao global de editar objetos
def editar_obj(request, modelo, modelo_formulario, mensagem, retorno_pag, id):
    objeto_edit = get_object_or_404(modelo, id=id)

    if request.method == 'POST':
        formulario_edit = modelo_formulario(request.POST, instance=objeto_edit)

        if formulario_edit.is_valid():
            formulario_edit.save()
            messages.success(request, mensagem)
            return redirect(retorno_pag)
        
    else:
        formulario_edit = modelo_formulario(instance=objeto_edit)

    return formulario_edit

# funçao global de editar usuario com 2 formulario (user, perfil)
def editar_user(request, id, modelo_bd, modelo_form_1, modelo_form_2, mensagem_1, retorno):

    perfil = get_object_or_404(modelo_bd, id=id)
    usuario_p = perfil.usuario

    if request.method == 'POST':
        formulario_edit_1 = modelo_form_1(request.POST, instance=usuario_p)
        formulario_edit_2 = modelo_form_2(request.POST, instance=perfil)

        if formulario_edit_1.is_valid() and formulario_edit_2.is_valid():
            formulario_edit_1.save()
            perfil_user = formulario_edit_2.save(commit=False)
            perfil_user.instituicao = perfil_user.campus.instituicao_campus
            perfil_user.save()
            messages.success(request, mensagem_1)
            return redirect(retorno)
        
        elif 'email' in formulario_edit_1.errors:
            messages.error(request, 'Erro ao editar usuário: E-mail inválido')

        else:
            messages.error(request, 'Erro ao editar usuário: Matrícula já existente')
        
    else:
        formulario_edit_1 = modelo_form_1(instance=usuario_p)
        formulario_edit_2 = modelo_form_2(instance=perfil)

    return formulario_edit_1, formulario_edit_2

# funçao global de editar foto de perfil do usuario
def editar_foto(request, modelo, modelo_formulario, mensagem, retorno_pag):
    usuario = infor_perfis(request, modelo)

    if request.method == 'POST':
        # gera um formulario a partir do modelo fornecido instanciado pelo usuario logado e salva as alteraçoes
        formulario = modelo_formulario(request.POST, request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, mensagem)
            return redirect(retorno_pag)
        
    # caso o formulario nao seja post gera apenas o o formulario
    else:
        formulario = modelo_formulario()

    return formulario

# funçao global de deletar foto de perfil do usuario
def deletar_foto_perfil(request, id, modelo, mensagem_1, mensagem_2):
    # procura um perfil pelo id a partir do model PerfilAdmin e que esteja logado ou 404
    perfil = get_object_or_404(modelo, id=id, usuario=request.user)
    
    # se o perfil tiver foto
    if perfil.foto_perfil:
        # sera deletado e salvo as alterações
        perfil.foto_perfil.delete()
        perfil.save()
        messages.success(request, mensagem_1)

    else:
        messages.error(request, mensagem_2)

    return perfil

# funçao global de redefinir senha do usuario
def redefinir_senha(request, modelo_formulario, nova_senha, confirm_senha, mensagem_1, mensagem_2, mensagem_3, retorno_pag):

    # se a requisição do formulario de cadastro for post crie 
    # uma instância do formulário senhaAdminForms com os dados enviados pelo usuário.
    if request.method == 'POST':
        formulario = modelo_formulario(request.POST)
                
        # verifica se o formulario e valido
        if formulario.is_valid():

            # se as senhas nao forem iguais redirecione para a pag de redefinir_senha novamente
            if formulario.cleaned_data[nova_senha] != formulario.cleaned_data[confirm_senha]:
                # mensagem de erro
                messages.error(request, mensagem_1)
                return redirect (retorno_pag)
            
            # define qual usuário será alterado
            usuario = request.user

            # Atualizando a senha com segurança
            senha = formulario.cleaned_data[nova_senha]
            usuario.set_password(senha)
            usuario.save()

            update_session_auth_hash(request, usuario)

            messages.success(request, mensagem_2)
            return redirect(retorno_pag)
        
    else:
        formulario = modelo_formulario()

    return formulario

