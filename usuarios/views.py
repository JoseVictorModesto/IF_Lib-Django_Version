from django.shortcuts import render, redirect, get_object_or_404
from usuarios.forms import LoginForms, cadastroAdminForms, perfilAdminForm
from django.contrib.auth.models import User
from usuarios.models import PerfilAdmin
from django.contrib import auth
from django.contrib import messages
from usuarios.models import PerfilAdmin

# FUNÇÕES GLOBAIS

# funçao global de informlções basicas dos perfis
def infor_perfis(request):
    # puxa as informações do usuario a partir do model PerfilAdmin que esteja logado
    # caso o usuario recem criado nao tenha ainda uma tabela no bd o django cria uma para esse user
    perfil, perfil_creat = PerfilAdmin.objects.get_or_create(usuario=request.user)
    return perfil

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES USUÁRIOS

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
            messages.success(request, f'Usúario {matricula} logado com sucesso!')         
            return redirect('home')
        
        # caso contrario retorna uma mensagem de erro e redireciona para pag de login
        else:
            # mensagem de erro
            messages.error(request, f'Erro Login, matícula ou senha incorretos!')
            return redirect('login')
        
    # renderiza pagina de login
    return render(request, 'login/login.html', {'formulario_login':formulario_login})

# logout usuario
def logout(request):

    # logout (sair) da sessão de login
    auth.logout(request)
    
    #mensagem sucesso
    messages.success(request, f'Logout efetuado!')

    return redirect('home')

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ÚNICAS DE ADMIN + ADMIN

# pagina inicial do perfil
def perfil_admin(request):
    infor_admin = infor_perfis(request)

    return render(request, 'usuarios/admin/informacoes_admin.html', {'infor_admin':infor_admin})

# editar o proprio perfil do usuario
def editar_perfil(request):
    infor_admin = infor_perfis(request)

    if request.method == 'POST':
        # gera um formulario a partir do perfilAdminForm instanciado pelo usuario logado e salva as alteraçoes
        formulario = perfilAdminForm(request.POST, request.FILES, instance=infor_admin)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Perfil alterado com sucesso!')
            return redirect('editar_perfil')
        
    # caso o formulario nao seja post gera apenas o o formulario
    else:
        formulario = perfilAdminForm()

    return render(request, 'usuarios/admin/editar_perfil_adm.html', {'infor_admin': infor_admin, 'formulario': formulario})

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

    return redirect('editar_perfil')

# Função cadastrar novo user Admin e exibi-los
def cadastro_admin(request):
    infor_admin = infor_perfis(request)
    formulario_cadastro_admin = cadastroAdminForms()

    # se a requisição do formulario de cadastro for post crie 
    # uma instância do formulário cadastroAdminForms com os dados enviados pelo usuário.
    if request.method == 'POST':
        formulario_cadastro_admin = cadastroAdminForms(request.POST)
        
        # verifica se o formulario e valido
        if formulario_cadastro_admin.is_valid():

            # se as senhas nao forem iguais redirecione para a pag de cad novamente
            if formulario_cadastro_admin['senha_admin'].value() != formulario_cadastro_admin['confirmar_senha_admin'].value():
                # mensagem de erro
                messages.error(request, f'As senhas não são iguais')
                return redirect ('cadastro_admin')
            
            # adiciona as informações do formulario nas variaveis correspondentes
            matricula=formulario_cadastro_admin['matricula_admin'].value()
            nome = formulario_cadastro_admin['nome_admin'].value()
            email = formulario_cadastro_admin['email_admin'].value()
            senha = formulario_cadastro_admin['senha_admin'].value()

            # verifição se o usuario ja existe no banco de dados
            if User.objects.filter(username=matricula).exists():
                # mensagem erro
                messages.error(request, f'Usúario já existente')
                return redirect ('cadastro_admin')
            
            # cria o usuario ADMIN como superuser
            user_admin = User.objects.create_superuser(
                username=matricula,
                first_name=nome,
                email=email,
                password=senha,
            )

            # salva o novo admin no banco de dados
            user_admin.save()
            
            # mensagem de sucesso
            messages.error(request, f'Admin {nome} cadastrado com sucesso!')
            return redirect('cadastro_admin')
        
    # dados da tabela de cadastro de admin
    # filtra somente os super usuarios ou seja os admins
    admin_tab = User.objects.filter(is_superuser=True)

    return render(request, 'usuarios/admin/cad_admin.html', {
        'formulario_cadastro_admin':formulario_cadastro_admin,
        'admin_tab': admin_tab,
        'infor_admin':infor_admin
        })

# deletar algum usuario admin
def deletar_user_admin(request, id):
    # puxa e guarda um objeto pelo id ou retorna um erro 404
    admin_delet = get_object_or_404(User, id=id)
    # deleta esse objeto do banco de dados
    admin_delet.delete()
    
    messages.success(request, f'Admin deletado com sucesso!')

    return redirect('cadastro_admin')

# editar algum usuario admin
def editar_user_admin(request, id):
    infor_admin = infor_perfis(request)

    # buscar um objeto (nesse caso um User = usuario) atravez do id fornecido ou retorna um erro 404
    # se encontrar armazena na variavel admin_edit
    admin_edit = get_object_or_404(User, pk=id)

    if request.method == 'POST':
        # instancia um formulario de edição com base no cadastroAdminForms
        formulario_edit = cadastroAdminForms(request.POST)
        # Verifica se esse formulario e valido
        if formulario_edit.is_valid():

            # verifica se os valores das senha_admin e confirmar_senha_admin sao iguais
            if formulario_edit.cleaned_data['senha_admin'] != formulario_edit.cleaned_data['confirmar_senha_admin']:
                messages.error(request, 'As senhas não são iguais!')
                return redirect('editar_user_admin', id=id)
            
            # atualiza os dados de um usuário (admin_edit) com os valores que o usuario digitou no formulario de edição.
            # ja os deixando prontos para uso com o cleaned_data
            admin_edit.username = formulario_edit.cleaned_data['matricula_admin']
            admin_edit.first_name = formulario_edit.cleaned_data['nome_admin']
            admin_edit.email = formulario_edit.cleaned_data['email_admin']
            # Define uma nova senha com hash
            admin_edit.set_password(formulario_edit.cleaned_data['senha_admin'])
            
            # salva essas alterações no banco de dados
            admin_edit.save()

            messages.success(request, 'Informações de usuário salvas com sucesso!')
            return redirect('cadastro_admin')
        
    # se caso a requisição nao for post (como nesse caso get)
    # ao entrar na pag de edit a requisição não é do tipo POST, usuário está apenas acessando a 
    # página para editar os dados, mas ainda não clicou no botão de “salvar”
    else:
        formulario_edit = cadastroAdminForms(initial={
            # preenche o formulário de edit com valores iniciais carregado do modelo do usuario ja salvo.
            'matricula_admin': admin_edit.username,
            'nome_admin': admin_edit.first_name,
            'email_admin': admin_edit.email,
        })
        
    return render(request, 'usuarios/admin/editar_admin.html', {'formulario_edit_admin':formulario_edit, 'id':id, 'infor_admin':infor_admin})

# --------------------------------------------------------------------------------------------------------------------------

# FUNÇÕES ÚNICAS DE ADMIN + INSTITUIÇÃO

def cad_instituicao(request):
    
    infor_admin = infor_perfis(request)   
    return render(request, 'usuarios/admin/instituições_admin.html', {'infor_admin':infor_admin})
    