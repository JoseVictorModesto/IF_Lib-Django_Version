from django.shortcuts import render, redirect, get_object_or_404

from apps.conteudos.forms import part01ConteudoForm
from apps.conteudos.forms import part02TutorConteudoForm, part02AutoresConteudoForm
from apps.conteudos.forms import part03DescricaoForm
from apps.conteudos.forms import part04ImagenCapaForm, part04MidiasForm
from apps.conteudos.forms import part05AdicionaisForm
from apps.conteudos.forms import part06ReferenciasForm
from apps.conteudos.forms import ConteudoExternoForms

from apps.login_perfil.views import cadastrar_obj, editar_obj

from apps.user_bibliotecario.models import PerfilProfessor, PerfilAluno

from apps.conteudos.models import ConteudoAcademico, Autores, Midias, ConteudoAdicionais, Referencias, CaixaFavoritos, CaixaFavoritosExternos, ConteudoExterno

from django.contrib import messages

from django.views.decorators.http import require_http_methods, require_GET, require_POST

from apps.notificacao.views import notificacao

from django.http import HttpResponseRedirect

def verificar_auth_cad_cai(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')
    
    # hasattr - verifica se um objeto tem um determinado atributo 
    # True > se o atributo existe no objeto
    # False > se o atributo não existe
    aluno = hasattr(request.user, 'usuario_aluno')
    professor = hasattr(request.user, 'usuario_professor')

    if aluno or professor:
        pass

    else:
        messages.error(request, 'Você não tem permissão para acessar essa página!')
        return redirect('home')

def verificar_auth_tutor(request, id):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')

    conteudo_academico = get_object_or_404(ConteudoAcademico, id=id)
    professor_tutor = conteudo_academico.tutor_conteudo and conteudo_academico.tutor_conteudo.usuario == request.user

    if not professor_tutor:
        messages.error(request, 'Você não tem permissão para acessar essa página!')
        return redirect('home')
    
def verificar_auth_prof_ce(request, id):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')

    conteudo_externo = get_object_or_404(ConteudoExterno, id=id)
    professor_ce = conteudo_externo.criador and conteudo_externo.criador == request.user

    if not professor_ce:
        messages.error(request, 'Você não tem permissão para acessar essa página!')
        return redirect('home')

def verificar_auth_professor(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')

    if not hasattr(request.user, 'usuario_professor') or request.user.usuario_professor.tipo_user != 'professor':
        messages.error(request, 'Você não tem permição para acessar essa página!')
        return redirect('home')

# --------------------------------------------------------------------------------------------------------------------------

# Conteudo academicos
# --------------------------------------------------------------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def cad_cai(request):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth

    # inicia as variaveis como none (inexistentes) para nao causar erro independente do tipo de perfil acesssado ou atributos do usuario
    aluno = None
    professor = None
    instituicao = None
    campus = None
    curso = None

    # hasattr - verifica se o usuario logado (objeto) tem o atributo usuario_aluno
    if hasattr(request.user, 'usuario_aluno'):
        aluno = request.user.usuario_aluno
        instituicao_conteudo_a = aluno.instituicao
        campus_conteudo_a = aluno.campus
        curso_conteudo_a = aluno.curso

    # hasattr - verifica se o usuario logado (objeto) tem o atributo usuario_professor
    if hasattr(request.user, 'usuario_professor'):
        professor = request.user.usuario_professor
        instituicao_conteudo_p = professor.instituicao
        campus_conteudo_p = professor.campus

    if request.method == 'POST':
        formulario_conteudo_01 = part01ConteudoForm(request.POST)
        formulario_conteudo_02_tutor = part02TutorConteudoForm(request.POST)
        formulario_conteudo_02_autor = part02AutoresConteudoForm(request.POST)
        formulario_conteudo_03_descricao = part03DescricaoForm(request.POST)
        formulario_conteudo_04_igm_capa = part04ImagenCapaForm(request.POST, request.FILES)
        formulario_conteudo_04_igm_midias = part04MidiasForm(request.POST, request.FILES)
        formuçario_conteudo_05_adicionais = part05AdicionaisForm(request.POST, request.FILES)
        formulario_conteudo_06_referencias = part06ReferenciasForm(request.POST)


        if formulario_conteudo_01.is_valid() and formulario_conteudo_02_tutor.is_valid() and formulario_conteudo_02_autor.is_valid() and formulario_conteudo_03_descricao.is_valid() and formulario_conteudo_04_igm_capa.is_valid() and formulario_conteudo_04_igm_midias.is_valid() and formuçario_conteudo_05_adicionais.is_valid() and formulario_conteudo_06_referencias.is_valid():
            # salva primeira parte do formulario
            cad_conteudo = formulario_conteudo_01.save(commit=False)

            # salva o tutor na segunda parte do formulario
            # cleaned_data puxa os dados ja limpos (dentro dos padroes estabelecidos no formulario) e adiciona a uma variavel (nesse caso tutor)
            # estou usando o cleaned_data pois trata-se de formularios diferentes que pertecem a mesma tabela (model)
            tutor = formulario_conteudo_02_tutor.cleaned_data['tutor_conteudo'] # refere-se ao formulario
            cad_conteudo.tutor_conteudo = tutor # refere-se ao model

            # salva terceira parte do formulario descricao
            descricao = formulario_conteudo_03_descricao.cleaned_data['descricao_conteudo']
            cad_conteudo.descricao_conteudo = descricao

            # salva terceira parte do formulario texto
            texto = request.POST.get('texto_editor') # referece ao formulario
            cad_conteudo.texto_conteudo = texto # refere-se ao model

            # salva quarta parte do formulario imagem capa
            imagem_capa = formulario_conteudo_04_igm_capa.cleaned_data['img_capa_conteudo']
            cad_conteudo.img_capa_conteudo = imagem_capa
            
            if aluno:
                messages.success(request, 'Conteúdo enviado com sucesso! Obrigado por sua contribuição. Aguarde a validação do seu tutor 😊')
            elif professor:
                cad_conteudo.validado = True
                messages.success(request, 'Conteúdo enviado com sucesso! Obrigado por sua contribuição. 😊')
            cad_conteudo.save()
            
            # envia a notificaçao para o tutor do conteudo
            if aluno:
                notificacao_tutor = notificacao(request, cad_conteudo.tutor_conteudo.usuario, cad_conteudo, 'Você foi marcado como tutor(a) em um novo conteúdo acadêmico', f'Olá { cad_conteudo.tutor_conteudo.usuario.first_name }, parabéns! Você foi marcado como professor(a) tutor(a) no conteúdo “{ cad_conteudo.titulo }”. Dê uma olhada no material e veja se está tudo ok para que possamos validá-lo e publicar na plataforma! Sua contribuição é sempre bem-vinda.')
            if professor:
                pass

            # salva os autores na segunda parte do formulario
            for i in range(1,6):
                autor = formulario_conteudo_02_autor.cleaned_data.get(f'autor_0{i}') # referece ao formulario
                if autor:
                    novo_autor = Autores(conteudo_cai=cad_conteudo, autor=autor.usuario) # refere-se ao model
                    novo_autor.save()

                    # envia a notificaçao para os autores do conteudo
                    if aluno:
                        notificacao_autores_aluno = notificacao(request, novo_autor.autor, cad_conteudo, 'Você faz parte de um novo conteúdo acadêmico', f'Olá {novo_autor.autor.first_name}, você foi incluído(a) como autor(a) no conteúdo acadêmico "{cad_conteudo.titulo}". Aguarde a validação do conteúdo pelo seu tutor ou acesse o seu perfil na plataforma para visualizar os detalhes! Muito obrigado por sua contribuição.')
                    if professor:
                        notificacao_autores_professor = notificacao(request, novo_autor.autor, cad_conteudo, 'Você faz parte de um novo conteúdo acadêmico', f'Olá {novo_autor.autor.first_name}, você foi incluído(a) como autor(a) no conteúdo acadêmico "{cad_conteudo.titulo}". Seu conteúdo já esta postado na plataforma. Muito obrigado por sua contribuição.')

            # salva as imagens na quarta parte do formulario
            for i in range(1,9):
                imagens = formulario_conteudo_04_igm_midias.cleaned_data.get(f'imagem_{i}')
                if imagens:
                    nova_imagem = Midias(conteudo_cai=cad_conteudo, imagem_conteudo=imagens)
                    nova_imagem.save()

            # salva os conteudo adicionais na quinta parte do formulario
            for i in range(1,5):
                arquivo_adicional = formuçario_conteudo_05_adicionais.cleaned_data.get(f'arquivo_{i}')
                if arquivo_adicional:
                    novo_adicional = ConteudoAdicionais(conteudo_cai=cad_conteudo, arquivo=arquivo_adicional)
                    novo_adicional.save()

            # salva as referencias na sexta parte do formulario
            referencias = formulario_conteudo_06_referencias.cleaned_data['referencia']
            # lista que irá armazenar cada link (url) que o user digitar
            links_digitados = []

            # o for percorre todas as referencias digitadas pelo user
            # splitlines() - metodo de string que irá separar cada link (string) pela quebra de linha /n
            for i in referencias.split(';;'):
                # strip() - remove cada espaço (espaços em branco no inicio e fim de cada string)
                link = i.strip()
                if link:
                    # adiciona cada string (link) digitado a lista links_digitados
                    links_digitados.append(link)

            for i in links_digitados:
                nova_referencia = Referencias(conteudo_cai=cad_conteudo, referencia_conteudo=i)
                nova_referencia.save()
            
            return redirect('cad_cai')
        
        else:
            messages.error(request, f'Erro ao enviar conteúdo: Encontramos alguns erros no preenchimento. Corrija os campos destacados e tente novamente.')
        
    else:

        # initial - Preenche a primeira parte do formulario com as informaçoes de acordo com o tipo de usuario caso seja 'none' sera ignorado
        if aluno:
            formulario_conteudo_01 = part01ConteudoForm(initial={ 'campus_conteudo': campus_conteudo_a, 'instituicao_conteudo': instituicao_conteudo_a, 'curso_conteudo': curso_conteudo_a})

        elif professor:
            formulario_conteudo_01 = part01ConteudoForm(initial={ 'campus_conteudo': campus_conteudo_p, 'instituicao_conteudo': instituicao_conteudo_p })

        if aluno:
            formulario_conteudo_02_tutor = part02TutorConteudoForm()

        elif professor:
            formulario_conteudo_02_tutor = part02TutorConteudoForm(initial={'tutor_conteudo':f'{request.user.username} / {request.user.first_name}'})
        
        formulario_conteudo_02_autor = part02AutoresConteudoForm(initial={'autor_01':f'{request.user.username} / {request.user.first_name}'})
        formulario_conteudo_03_descricao = part03DescricaoForm()
        formulario_conteudo_04_igm_capa = part04ImagenCapaForm()
        formulario_conteudo_04_igm_midias = part04MidiasForm()
        formuçario_conteudo_05_adicionais = part05AdicionaisForm()
        formulario_conteudo_06_referencias = part06ReferenciasForm()

    # lista de tutores
    lista_tutores = PerfilProfessor.objects.all()
    # lista de autores
    lista_autores_alunos = PerfilAluno.objects.all()
    lista_autores = list(lista_autores_alunos) + list(lista_tutores)


    return render(request, 'conteudos/cad_cai.html', {'formulario_conteudo_01':formulario_conteudo_01, 
                                                      'formulario_conteudo_02_tutor':formulario_conteudo_02_tutor,
                                                      'formulario_conteudo_02_autor':formulario_conteudo_02_autor,
                                                      'formulario_conteudo_03_descricao':formulario_conteudo_03_descricao,
                                                      'formulario_conteudo_04_igm_capa':formulario_conteudo_04_igm_capa,
                                                      'formulario_conteudo_04_igm_midias':formulario_conteudo_04_igm_midias,
                                                      'formuçario_conteudo_05_adicionais':formuçario_conteudo_05_adicionais,
                                                      'formulario_conteudo_06_referencias':formulario_conteudo_06_referencias,
                                                      'lista_tutores': lista_tutores,
                                                      'lista_autores':lista_autores,})

@require_GET
def vizualizar_cai(request, id):

    aluno = hasattr(request.user, 'usuario_aluno')
    professor = hasattr(request.user, 'usuario_professor')

    conteudo_academico = get_object_or_404(ConteudoAcademico, id=id)
    autores_conteudo = Autores.objects.filter(conteudo_cai=conteudo_academico).order_by('autor__first_name')
    midias_conteudo = Midias.objects.filter(conteudo_cai=conteudo_academico)
    adicionais_conteudo = ConteudoAdicionais.objects.filter(conteudo_cai=conteudo_academico)
    referencias_conteudo = Referencias.objects.filter(conteudo_cai=conteudo_academico)

    favorito = None
    if request.user.is_authenticated:
        favorito = CaixaFavoritos.objects.filter(conteudo_cai=conteudo_academico, usuario=request.user)

    return render(request, 'conteudos/vizualizar_cai.html', {'id':id, 'conteudo_academico':conteudo_academico, 
                                                             'autores_conteudo':autores_conteudo,
                                                             'midias_conteudo':midias_conteudo,
                                                             'adicionais_conteudo':adicionais_conteudo,
                                                             'referencias_conteudo':referencias_conteudo,
                                                             'aluno':aluno,
                                                             'professor':professor,
                                                             'favorito':favorito})

@require_http_methods(["GET", "POST"])
def vizualizar_cai_nao_valid(request, id):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth

    conteudo_academico = get_object_or_404(ConteudoAcademico, id=id)
    autores_conteudo = Autores.objects.filter(conteudo_cai=conteudo_academico).order_by('autor__first_name')
    midias_conteudo = Midias.objects.filter(conteudo_cai=conteudo_academico)
    adicionais_conteudo = ConteudoAdicionais.objects.filter(conteudo_cai=conteudo_academico)
    referencias_conteudo = Referencias.objects.filter(conteudo_cai=conteudo_academico)

    professor_tutor = conteudo_academico.tutor_conteudo and conteudo_academico.tutor_conteudo.usuario == request.user
    autor = Autores.objects.filter(conteudo_cai=conteudo_academico, autor=request.user).exists()

    if professor_tutor or autor:
        pass

    else:
        messages.error(request, 'Você não tem permição para acessar essa página!')
        return redirect('home')

    return render(request, 'conteudos/vizualizar_cai_nao_valid.html', {'id':id, 'conteudo_academico':conteudo_academico, 
                                                             'autores_conteudo':autores_conteudo,
                                                             'midias_conteudo':midias_conteudo,
                                                             'adicionais_conteudo':adicionais_conteudo,
                                                             'referencias_conteudo':referencias_conteudo,
                                                             'professor_tutor':professor_tutor,
                                                             'autor':autor})

@require_POST
def validar_cai(request, id):
    usuario_auth = verificar_auth_tutor(request, id)
    if usuario_auth:
        return usuario_auth
    
    conteudo_cai = get_object_or_404(ConteudoAcademico, id=id)
    conteudo_cai.validado = True
    conteudo_cai.save()

    autores = Autores.objects.filter(conteudo_cai=conteudo_cai)

    for i in autores:
        notificacao_valid = notificacao(request, i.autor, conteudo_cai, 'Conteúdo validado com sucesso!', f'Olá {i.autor.first_name} meus parabéns, seu conteúdo acadêmico "{conteudo_cai.titulo}" acabou de ser aprovado pelo tutor e já esta no ar na plataforma, muito obrigado por sua contribuição!')

    messages.success(request, 'Conteúdo validado com sucesso!')
    return redirect('vizualizar_cai', id=conteudo_cai.id)

@require_http_methods(["GET", "POST"])
def revisao_cai(request, id):
    usuario_auth = verificar_auth_tutor(request, id)
    if usuario_auth:
        return usuario_auth

    conteudo_a_revisar = get_object_or_404(ConteudoAcademico, id=id)

    if request.method == 'POST':
        # descriçao de revisao
        texto_revisao = request.POST.get('texto_editor_revisao') # informaçoes do quill

        autores = Autores.objects.filter(conteudo_cai=conteudo_a_revisar)
        
        for i in autores:
            notificacao_revisao = notificacao(request, i.autor, conteudo_a_revisar, f'Seu conteúdo "{ conteudo_a_revisar.titulo }" precisa de ajustes. Por favor, revise e tente novamente.', texto_revisao)
            
        messages.success(request, 'Revisão de contúdo envida com sucesso!')
        return redirect('vizualizar_cai_nao_valid', id=conteudo_a_revisar.id)
    
    return render(request, 'conteudos/revisao_cai.html', {'conteudo_a_revisar':conteudo_a_revisar, 'id':conteudo_a_revisar.id})

@require_http_methods(["GET", "POST"])
def editar_cai(request, id):

    conteudo_edit = get_object_or_404(ConteudoAcademico, id=id)
    autores_cai = Autores.objects.filter(conteudo_cai=conteudo_edit)
    midias_cai = Midias.objects.filter(conteudo_cai=conteudo_edit)
    adicionais_cai = ConteudoAdicionais.objects.filter(conteudo_cai=conteudo_edit)
    referencias_cai = Referencias.objects.filter(conteudo_cai=conteudo_edit)

    # inicia as variaveis como none (inexistentes) para nao causar erro independente do tipo de perfil acesssado ou atributos do usuario
    aluno = None
    professor = None
    instituicao = None
    campus = None
    curso = None

    # hasattr - verifica se o usuario logado (objeto) tem o atributo usuario_aluno
    if hasattr(request.user, 'usuario_aluno'):
        aluno = request.user.usuario_aluno
        instituicao_conteudo_a = aluno.instituicao
        campus_conteudo_a = aluno.campus
        curso_conteudo_a = aluno.curso

    # hasattr - verifica se o usuario logado (objeto) tem o atributo usuario_professor
    if hasattr(request.user, 'usuario_professor'):
        professor = request.user.usuario_professor
        instituicao_conteudo_p = professor.instituicao
        campus_conteudo_p = professor.campus

    if request.method == 'POST':
        formulario_conteudo_01 = part01ConteudoForm(request.POST, instance=conteudo_edit)
        formulario_conteudo_02_tutor = part02TutorConteudoForm(request.POST)
        formulario_conteudo_02_autor = part02AutoresConteudoForm(request.POST)
        formulario_conteudo_03_descricao = part03DescricaoForm(request.POST, instance=conteudo_edit)
        formulario_conteudo_04_igm_capa = part04ImagenCapaForm(request.POST, request.FILES, instance=conteudo_edit)
        formulario_conteudo_04_igm_midias = part04MidiasForm(request.POST, request.FILES)
        formuçario_conteudo_05_adicionais = part05AdicionaisForm(request.POST, request.FILES)
        formulario_conteudo_06_referencias = part06ReferenciasForm(request.POST)

        if formulario_conteudo_01.is_valid() and formulario_conteudo_02_tutor.is_valid() and formulario_conteudo_02_autor.is_valid() and formulario_conteudo_03_descricao.is_valid() and formulario_conteudo_04_igm_capa.is_valid() and formulario_conteudo_04_igm_midias.is_valid() and formuçario_conteudo_05_adicionais.is_valid() and formulario_conteudo_06_referencias.is_valid():
            # salva primeira parte do formulario
            cad_conteudo = formulario_conteudo_01.save(commit=False)

            # salva o tutor na segunda parte do formulario
            # cleaned_data puxa os dados ja limpos (dentro dos padroes estabelecidos no formulario) e adiciona a uma variavel (nesse caso tutor)
            # estou usando o cleaned_data pois trata-se de formularios diferentes que pertecem a mesma tabela (model)
            tutor = formulario_conteudo_02_tutor.cleaned_data['tutor_conteudo'] # refere-se ao formulario
            cad_conteudo.tutor_conteudo = tutor # refere-se ao model

            # salva terceira parte do formulario descricao
            descricao = formulario_conteudo_03_descricao.cleaned_data['descricao_conteudo']
            cad_conteudo.descricao_conteudo = descricao

            # salva terceira parte do formulario texto
            texto = request.POST.get('texto_editor_editar_cont') # referece ao formulario
            cad_conteudo.texto_conteudo = texto # refere-se ao model

            # salva quarta parte do formulario imagem capa
            imagem_capa = formulario_conteudo_04_igm_capa.cleaned_data['img_capa_conteudo']
            cad_conteudo.img_capa_conteudo = imagem_capa

            messages.success(request, 'Conteúdo editado com sucesso! Aguarde o retorno do seu tutor 😊')
            cad_conteudo.save()
            
            # envia a notificaçao para o tutor do conteudo
            notificacao_tutor = notificacao(request, cad_conteudo.tutor_conteudo.usuario, cad_conteudo, 'Conteúdo acadêmico revisado', f'O conteúdo “{ cad_conteudo.titulo } sofreu algumas alterações”. Dê uma olhada no material e veja se está tudo ok para que possamos validá-lo e publicar na plataforma! Sua contribuição é sempre bem-vinda.')

            # salva os autores na segunda parte do formulario
            for i in range(1,6):
                autor = formulario_conteudo_02_autor.cleaned_data.get(f'autor_0{i}') # referece ao formulario
                if autor:
                    novo_autor = Autores(conteudo_cai=cad_conteudo, autor=autor.usuario) # refere-se ao model
                    novo_autor.save()

                    # envia a notificaçao para os autores do conteudo
                    if aluno:
                        notificacao_autores_aluno = notificacao(request, novo_autor.autor, cad_conteudo, 'Você faz parte de um novo conteúdo acadêmico', f'Olá {novo_autor.autor.first_name}, você foi incluído(a) como autor(a) no conteúdo acadêmico "{cad_conteudo.titulo}". Aguarde a validação do conteúdo pelo seu tutor ou acesse o seu perfil na plataforma para visualizar os detalhes! Muito obrigado por sua contribuição.')
                    if professor:
                        notificacao_autores_professor = notificacao(request, novo_autor.autor, cad_conteudo, 'Você faz parte de um novo conteúdo acadêmico', f'Olá {novo_autor.autor.first_name}, você foi incluído(a) como autor(a) no conteúdo acadêmico "{cad_conteudo.titulo}". Seu conteúdo já esta postado na plataforma. Muito obrigado por sua contribuição.')

            # salva as imagens na quarta parte do formulario
            for i in range(1,9):
                imagens = formulario_conteudo_04_igm_midias.cleaned_data.get(f'imagem_{i}')
                if imagens:
                    nova_imagem = Midias(conteudo_cai=cad_conteudo, imagem_conteudo=imagens)
                    nova_imagem.save()

            # salva os conteudo adicionais na quinta parte do formulario
            for i in range(1,5):
                arquivo_adicional = formuçario_conteudo_05_adicionais.cleaned_data.get(f'arquivo_{i}')
                if arquivo_adicional:
                    novo_adicional = ConteudoAdicionais(conteudo_cai=cad_conteudo, arquivo=arquivo_adicional)
                    novo_adicional.save()

            # salva as referencias na sexta parte do formulario
            referencias = formulario_conteudo_06_referencias.cleaned_data['referencia']
            # lista que irá armazenar cada link (url) que o user digitar
            links_digitados = []

            # o for percorre todas as referencias digitadas pelo user
            # splitlines() - metodo de string que irá separar cada link (string) pela quebra de linha /n
            for i in referencias.split(';;'):
                # strip() - remove cada espaço (espaços em branco no inicio e fim de cada string)
                link = i.strip()
                if link:
                    # adiciona cada string (link) digitado a lista links_digitados
                    links_digitados.append(link)

            for i in links_digitados:
                nova_referencia = Referencias(conteudo_cai=cad_conteudo, referencia_conteudo=i)
                nova_referencia.save()
            
            return redirect('cad_cai')
        
        else:
            messages.error(request, f'Erro ao enviar conteúdo: Encontramos alguns erros no preenchimento. Corrija os campos destacados e tente novamente.')
        
    else:
        # Parte 01 e outras que usam ModelForm continuam com instance normalmente
        formulario_conteudo_01 = part01ConteudoForm(instance=conteudo_edit)
        formulario_conteudo_02_tutor = part02TutorConteudoForm(initial={'tutor_conteudo':conteudo_edit.tutor_conteudo})
        formulario_conteudo_03_descricao = part03DescricaoForm(instance=conteudo_edit)
        formulario_conteudo_04_igm_capa = part04ImagenCapaForm(initial={'img_capa_conteudo':conteudo_edit.img_capa_conteudo})

        # Parte 02 - Autores (preenche via initial)
        autores_iniciais = {}
        for i, autor in enumerate(autores_cai[:5]):
            autores_iniciais[f'autor_0{i+1}'] = autor.autor

        formulario_conteudo_02_autor = part02AutoresConteudoForm(initial=autores_iniciais)

        # Parte 04 - Mídias (preenche via initial)
        midias_iniciais = {}
        for i, midia in enumerate(midias_cai[:8]):
            midias_iniciais[f'imagem_{i+1}'] = midia.imagem_conteudo

        formulario_conteudo_04_igm_midias = part04MidiasForm(initial=midias_iniciais)

        # Parte 05 - Adicionais
        adicionais_iniciais = {}
        for i, adicional in enumerate(adicionais_cai[:4]):
            adicionais_iniciais[f'arquivo_{i+1}'] = adicional.arquivo

        formuçario_conteudo_05_adicionais = part05AdicionaisForm(initial=adicionais_iniciais)

        # Parte 06 - Referências
        referencias_texto = ';;'.join([ref.referencia_conteudo for ref in referencias_cai])
        formulario_conteudo_06_referencias = part06ReferenciasForm(initial={'referencia': referencias_texto})

    # lista de tutores
    lista_tutores = PerfilProfessor.objects.all()
    # lista de autores
    lista_autores_alunos = PerfilAluno.objects.all()
    lista_autores = list(lista_autores_alunos) + list(lista_tutores)


    return render(request, 'conteudos/editar_cai.html', {'formulario_conteudo_01':formulario_conteudo_01, 
                                                      'formulario_conteudo_02_tutor':formulario_conteudo_02_tutor,
                                                      'formulario_conteudo_02_autor':formulario_conteudo_02_autor,
                                                      'formulario_conteudo_03_descricao':formulario_conteudo_03_descricao,
                                                      'formulario_conteudo_04_igm_capa':formulario_conteudo_04_igm_capa,
                                                      'formulario_conteudo_04_igm_midias':formulario_conteudo_04_igm_midias,
                                                      'formuçario_conteudo_05_adicionais':formuçario_conteudo_05_adicionais,
                                                      'formulario_conteudo_06_referencias':formulario_conteudo_06_referencias,
                                                      'lista_tutores': lista_tutores,
                                                      'lista_autores':lista_autores,
                                                      'id':conteudo_edit.id})

# Conteudo externos
# --------------------------------------------------------------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def cad_externo(request):
    usuario_auth = verificar_auth_professor(request)
    if usuario_auth:
        return usuario_auth

    formulario_ce = cadastrar_obj(request, ConteudoExternoForms, 'Conteúdo postado com sucesso! Obrigado por sua contribuição. 😊', 'Erro ao cadastrar a conteúdo.', 'cad_externo')

    if isinstance(formulario_ce, HttpResponseRedirect):
        return formulario_ce

    return render(request, 'conteudos/cad_ce.html', {'formulario_ce':formulario_ce})

@require_http_methods(["GET", "POST"])
def editar_externo(request, id):
    usuario_auth = verificar_auth_prof_ce(request, id)
    if usuario_auth:
        return usuario_auth
    
    formulario_edit = editar_obj(request, ConteudoExterno, ConteudoExternoForms, 'Conteúdo editado com sucesso!', 'perfil_professor', id)

    if isinstance(formulario_edit, HttpResponseRedirect):
        return formulario_edit

    return render(request, 'conteudos/editar_ce.html', {'formulario_edit':formulario_edit, 'id':id})

@require_GET
def vizualizar_ce(request, id):

    aluno = hasattr(request.user, 'usuario_aluno')
    professor = hasattr(request.user, 'usuario_professor')

    conteudo_externo = get_object_or_404(ConteudoExterno, id=id)
    professor_ce = ConteudoExterno.objects.none()
    if request.user.is_authenticated:
        professor_ce = ConteudoExterno.objects.filter(criador=request.user)

    favorito = ConteudoExterno.objects.none()
    if request.user.is_authenticated:
        favorito = CaixaFavoritosExternos.objects.filter(conteudo_ce=conteudo_externo, usuario=request.user)

    return render(request, 'conteudos/vizualizar_ce.html', {'id':id, 'conteudo_externo':conteudo_externo, 'professor_ce':professor_ce, 'aluno':aluno, 'professor':professor, 'favorito':favorito})

# Favoritos
# --------------------------------------------------------------------------------------------------------------------------

def caixa_favoritos(request):
    caixa, criar_caixa = CaixaFavoritos.objects.get_or_create(usuario=request.user)
    return caixa

def caixa_favoritos_ex(request):
    caixa, criar_caixa_ex = CaixaFavoritosExternos.objects.get_or_create(usuario=request.user)
    return caixa

@require_POST
def salvar_favorito(request, id):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth

    caixa_user = caixa_favoritos(request)
    conteudo_favoritar = get_object_or_404(ConteudoAcademico, id=id)
    caixa_user.conteudo_cai.add(conteudo_favoritar)
    messages.success(request, 'Conteúdo favoritado com sucesso!')

    conteudo_favoritar.qtd_favoritos = conteudo_favoritar.qtd_favoritos + 1
    conteudo_favoritar.save()

    return redirect('vizualizar_cai', id=conteudo_favoritar.id)

@require_POST
def salvar_favorito_ex(request, id):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth

    caixa_user = caixa_favoritos_ex(request)
    conteudo_favoritar = get_object_or_404(ConteudoExterno, id=id)
    caixa_user.conteudo_ce.add(conteudo_favoritar)
    messages.success(request, 'Conteúdo favoritado com sucesso!')

    conteudo_favoritar.qtd_favoritos = conteudo_favoritar.qtd_favoritos + 1
    conteudo_favoritar.save()

    return redirect('vizualizar_ce', id=conteudo_favoritar.id)

@require_POST
def remover_favorito_ex(request, id):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth
    
    caixa_user = caixa_favoritos_ex(request)
    conteudo_desfavoritar = get_object_or_404(ConteudoExterno, id=id)
    caixa_user.conteudo_ce.remove(conteudo_desfavoritar)
    messages.success(request, 'Conteúdo removido dos favoritos!')

    conteudo_desfavoritar.qtd_favoritos = conteudo_desfavoritar.qtd_favoritos - 1
    conteudo_desfavoritar.save()

    return redirect('vizualizar_ce', id=conteudo_desfavoritar.id)

@require_POST
def remover_favorito(request, id):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth
    
    caixa_user = caixa_favoritos(request)
    conteudo_desfavoritar = get_object_or_404(ConteudoAcademico, id=id)
    caixa_user.conteudo_cai.remove(conteudo_desfavoritar)
    messages.success(request, 'Conteúdo removido dos favoritos!')

    conteudo_desfavoritar.qtd_favoritos = conteudo_desfavoritar.qtd_favoritos - 1
    conteudo_desfavoritar.save()

    return redirect('vizualizar_cai', id=conteudo_desfavoritar.id)

@require_GET
def todos_favorito(request):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth
    
    minha_caixa = caixa_favoritos(request)
    meus_cai_favoritos = minha_caixa.conteudo_cai.all().order_by('titulo')

    return render(request, 'conteudos/caixa_favoritos.html', {'meus_cai_favoritos':meus_cai_favoritos})

@require_GET
def todos_favorito_ex(request):
    usuario_auth = verificar_auth_cad_cai(request)
    if usuario_auth:
        return usuario_auth
    
    minha_caixa = caixa_favoritos_ex(request)
    meus_ce_favoritos = minha_caixa.conteudo_ce.all().order_by('titulo')

    return render(request, 'conteudos/caixa_favoritos_ex.html', {'meus_ce_favoritos':meus_ce_favoritos})