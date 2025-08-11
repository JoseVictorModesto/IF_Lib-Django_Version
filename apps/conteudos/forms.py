from django import forms

from apps.conteudos.models import ConteudoAcademico, ConteudoExterno

from apps.user_bibliotecario.models import PerfilProfessor, PerfilAluno


from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# formulario conteudo parte 01
class part01ConteudoForm(forms.ModelForm):
    class Meta:
        model = ConteudoAcademico
        fields = ['titulo', 'instituicao_conteudo', 'campus_conteudo', 'curso_conteudo', 'categoria_conteudo', 'tipos_conteudo']

        labels = {
            'titulo':'Título *',
            'instituicao_conteudo':'Instituição *',
            'campus_conteudo':'Campus *',
            'curso_conteudo':'Curso *',
            'categoria_conteudo':'Categoria *',
            'tipos_conteudo':'Tipo *',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o título do conteúdo:'}),
            'instituicao_conteudo': forms.Select(attrs={'class':'input_cad'}),
            'campus_conteudo': forms.Select(attrs={'class':'input_cad'}),
            'curso_conteudo': forms.Select(attrs={'class':'input_cad'}),
            'categoria_conteudo': forms.Select(attrs={'class':'input_cad'}),
            'tipos_conteudo': forms.Select(attrs={'class':'input_cad'}),
        }

    # informa uma descriçao aos selects
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instituicao_conteudo'].empty_label = "Selecione uma instituição:"
        self.fields['campus_conteudo'].empty_label = "Selecione um campus:"
        self.fields['curso_conteudo'].empty_label = "Selecione um curso:"
        self.fields['categoria_conteudo'].empty_label = "Selecione uma categoria:"
        self.fields['tipos_conteudo'].empty_label = "Selecione um tipo:"

# formulario conteudo parte 02 (tutor)
class part02TutorConteudoForm(forms.Form):
    # Tutor
    tutor_conteudo = forms.CharField(
        label = 'Professor Tutor *',
        required=True,
        widget=forms.TextInput(
            attrs={'class':'input_cad', 'placeholder':'Digite ou selecione a matrícula do professor tutor', 'list':'lista_tutores'}
        )
    )
        
    # verifica se as informaçoes passadas estao de acordo com as regras estabelecidas pelo formulario
    def clean_tutor_conteudo(self):

        # self.cleaned_data - pega e armazena os dados ja verificados que foram digitados no input e armazena na variavel tutor
        tutor = self.cleaned_data['tutor_conteudo']
        # split() - Extrai somente o username (matricula) antes da barra / strip() - remove os espaços
        username_matricula = tutor.split(' / ')[0].strip()
        
        # verifica se o tutor realmente exite, caso nao exita, retorna a msg de professor nao encontrado
        try:
            # puxa o objeto usuario atraves do username
            tutor = PerfilProfessor.objects.get(usuario__username=username_matricula)
            return tutor

        except PerfilProfessor.DoesNotExist:
            raise forms.ValidationError('Professor tutor não encontrado.')

# formulario conteudo parte 02 (autores)
class part02AutoresConteudoForm(forms.Form):
    # autores
    autor_01 = forms.CharField(
        label='Autor 01 *',
        required=True,
        widget=forms.TextInput(
            attrs={'class':'input_cad', 'placeholder':'Digite ou selecione a matrícula do autor', 'list':'lista_autores'}
        )
    )

    autor_02 = forms.CharField(
        label='Autor 02',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'input_cad', 'placeholder':'Digite ou selecione a matrícula do autor', 'list':'lista_autores'}
        )
    )

    autor_03 = forms.CharField(
        label='Autor 03',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'input_cad', 'placeholder':'Digite ou selecione a matrícula do autor', 'list':'lista_autores'}
        )
    )

    autor_04 = forms.CharField(
        label='Autor 04',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'input_cad', 'placeholder':'Digite ou selecione a matrícula do autor', 'list':'lista_autores'}
        )
    )

    autor_05 = forms.CharField(
        label='Autor 05',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'input_cad', 'placeholder':'Digite ou selecione a matrícula do autor', 'list':'lista_autores'}
        )
    )

    # verifica se as informaçoes passadas estao de acordo com as regras estabelecidas pelo formulario
    def clean_autor_01(self):
        return self.verificar_autor('autor_01')
    
    def clean_autor_02(self):
        return self.verificar_autor('autor_02')
    
    def clean_autor_03(self):
        return self.verificar_autor('autor_03')

    def clean_autor_04(self):
        return self.verificar_autor('autor_04')

    def clean_autor_05(self):
        return self.verificar_autor('autor_05')
    
    # verifica tanto na tabela de alunos quanto de professor se exite o objeto, caso nao encontre retorna a msg de autor nao encontrado
    def verificar_autor(self, campos_autores):
        matricula_autor = self.cleaned_data.get(campos_autores)

        username_matricula_autor = matricula_autor.split(' / ')[0].strip()

        if not matricula_autor:
            return None
    
        try:
            autor = PerfilAluno.objects.get(usuario__username=username_matricula_autor)
            return autor
            
        except PerfilAluno.DoesNotExist:
            pass


        try:
            autor = PerfilProfessor.objects.get(usuario__username=username_matricula_autor)
            return autor
            
        except PerfilProfessor.DoesNotExist:
            raise forms.ValidationError('Autor não encontrado.')
        
    # Validação para evitar duplicidade
    def clean(self):
        cleaned_data = super().clean()

        # lista de nomes dos campos de autores
        campos = ['autor_01', 'autor_02', 'autor_03', 'autor_04', 'autor_05']
        
        # pega os valores de todos os campos de autores
        autores = [
            cleaned_data.get('autor_01'),
            cleaned_data.get('autor_02'),
            cleaned_data.get('autor_03'),
            cleaned_data.get('autor_04'),
            cleaned_data.get('autor_05'),
        ]

        # Remove campos vazios (None)
        autores_validos = []
        for i in autores:
            if i is not None:
                autores_validos.append(i)

        # Extrai os username dos autores
        autores_username = []
        for i in autores_validos:
            # adiciona o username dos usuarios PerfilAluno ou PerfilProfessor a lista autores_username
            autores_username.append(i.usuario.username)


        # Verifica se o autor foi digitado mais de uma vez
        usuarios_repetidos = []
        for i in autores_username:
            if autores_username.count(i) > 1:
                usuarios_repetidos.append(i)

        duplicados = set(usuarios_repetidos)

        # Marca erro nos campos dos autores repetidos
        if duplicados:
            for i, autor in enumerate(autores):
                if autor and autor.usuario.username in duplicados:
                    self.add_error(campos[i], "Autor marcado mais de uma vez.")

        return cleaned_data

# formulario conteudo parte 03 (descrição)     
class part03DescricaoForm(forms.ModelForm):
    class Meta:
        model = ConteudoAcademico
        fields = ['descricao_conteudo']

        labels = {
            'descricao_conteudo':'Descrição *'
        }


        widgets = {
            'descricao_conteudo': forms.TextInput(attrs={'class':'input_cad input_text', 'placeholder': 'Digite uma breve descrição do conteúdo:'}),
        }

# formulario conteudo parte 04 (imagem de capa)
class part04ImagenCapaForm(forms.ModelForm):
    class Meta:
        model = ConteudoAcademico
        fields = ['img_capa_conteudo']

        labels = {
            'img_capa_conteudo':'Imagem de capa',
        }

        widgets = {
            'img_capa_conteudo': forms.FileInput(attrs={'class':'img_edit img_capa',})
        }

# formulario conteudo parte 04 (imagens adicionais)
class part04MidiasForm(forms.Form):
    # midias adicionais (imagens)
    imagem_1 = forms.ImageField(
        label='Imagem adicional 01',
        required=False,
        widget=forms.FileInput(attrs={'class':'adc_mais',})
    )

    imagem_2 = forms.ImageField(
        label='Imagem adicional 02',
        required=False,
        widget= forms.FileInput(attrs={'class':'adc_mais',})
    )

    imagem_3 = forms.ImageField(
        label='Imagem adicional 03',
        required=False,
        widget=forms.FileInput(attrs={'class':'adc_mais',})
    )

    imagem_4 = forms.ImageField(
        label='Imagem adicional 04',
        required=False,
        widget=forms.FileInput(attrs={'class':'adc_mais',})
    )

    imagem_5 = forms.ImageField(
        label='Imagem adicional 05',
        required=False,
        widget=forms.FileInput(attrs={'class':'adc_mais'})
    )

    imagem_6 = forms.ImageField(
        label='Imagem adicional 06',
        required=False,
        widget=forms.FileInput(attrs={'class':'adc_mais'})
    )

    imagem_7 = forms.ImageField(
        label='Imagem adicional 07',
        required=False,
        widget=forms.FileInput(attrs={'class':'adc_mais'})
    )

    imagem_8 = forms.ImageField(
        label='Imagem adicional 08',
        required=False,
        widget=forms.FileInput(attrs={'class':'adc_mais'})
    )

# formulario conteudo parte 05 (arquivos adicionais)
class part05AdicionaisForm(forms.Form):
    arquivo_1 = forms.FileField(
        label='Arquivo adicional 01',
        required=False,
        widget=forms.FileInput(attrs={'class':'form_doc'})
    )

    arquivo_2 = forms.FileField(
        label='Arquivo adicional 02',
        required=False,
        widget=forms.FileInput(attrs={'class':'form_doc'})
    )

    arquivo_3 = forms.FileField(
        label='Arquivo adicional 03',
        required=False,
        widget=forms.FileInput(attrs={'class':'form_doc'})
    )

    arquivo_4 = forms.FileField(
        label='Arquivo adicional 04',
        required=False,
        widget=forms.FileInput(attrs={'class':'form_doc'})
    )

    # clean / verifica e valida os dados do formulario
    def clean(self):

        # armzena como um dicionario os dados limpos coletados dos formularios da super classe / classe mãe (part05AdicionaisForm)
        dados_formulario = super().clean()

        # tipos de arquivos permitidos
        arquivos_validos = ['.pdf', '.doc', '.docx', '.odt', '.txt']

        for i in range(1, 5):
            arquivo = dados_formulario.get(f'arquivo_{i}')
            if arquivo:
                # captura o nome do arquivo e o lower() converte tudo para letras minusculas e armazena na veriavel
                nome_arquivo = arquivo.name.lower()
                # o loop for percorre todos os tipos de aquivos validos e a funcao endswith() verifica o nome de cada 
                # arquivo entregue pelo formulario termina, e a funcao any verifica se é igual aos tipos entregues pela variavel arquivos_validos[]
                # caso nao seja igual ao tipos validos retorna um False, se estiver dentro do padrão retorna true
                if not any(nome_arquivo.endswith(j) for j in arquivos_validos):
                    self.add_error(f'arquivo_{i}', 'Tipo de arquivo não permitido')

# formulario conteudo parte 06 (referencias)
class part06ReferenciasForm(forms.Form):
    referencia = forms.CharField(
        label='Referências',
        required=True,
        widget=forms.TextInput(attrs={'class':'input_cad input_text ref_input', 'placeholder': 'Cole aqui os links de referèncias. Obs use dois ponto e vígulas para separar os links( ;; )'})
    )

    def clean_referencia(self):
        # armazena os dados ja 'limpos' dentro da variavel (lista) referencias_digitadas
        referencias_digitadas = self.cleaned_data['referencia']

        # verifica se a url e valida
        verificar_link = URLValidator()
        # percorre a lista de link digitados pelo user separando cada link atravez da quebra de linha
        for i in referencias_digitadas.split(';;'):
            # strip() - remove cada espaço (espaços em branco no inicio e fim de cada string)
            link = i.strip()
            if link:
                try:
                    # verfica cada link da lista
                    verificar_link(link)

                # caso algum deles seja invalido o raise para o for e exibe a msg de erro
                except ValidationError:
                    raise ValidationError(f'O link digitado: "{i}" não é válido. Verifique e tente novamente.')
            
        return referencias_digitadas

# formulario conteudo externo
class ConteudoExternoForms(forms.ModelForm):
    class Meta:
        model = ConteudoExterno
        fields = ['img_capa', 'titulo', 'descricao_conteudo', 'link_conteudo']

        labels = {
            'img_capa':'Imagem de capa',
            'titulo':'Título *',
            'descricao_conteudo':'Descrição *',
            'link_conteudo':'Link do conteúdo *'
        }

        widgets = {
            'img_capa': forms.FileInput(attrs={'class':'img_edit img_capa'}),
            'titulo': forms.TextInput(attrs={'class':'input_cad input_text_ex', 'placeholder': 'Digite o título do conteúdo:'}),
            'descricao_conteudo': forms.Textarea(attrs={'class':'input_cad input_text_ex desc_ext', 'placeholder': 'Digite a descrição do conteúdo:'}),
            'link_conteudo': forms.URLInput(attrs={'class':'input_cad input_text_ex', 'placeholder': 'Informe o link de acesso:'})
        }
