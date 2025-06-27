from django import forms


from django.contrib.auth.models import User

from apps.user_admin.models import PerfilAdmin, Instituicao, Curso, Campus, Categoria, Tipos, PerfilBibliotecario

# formulario de cadastro Admin   

class cadastroAdminForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {
            'username':'Matrícula:',
            'first_name':'Nome:',
            'email':'E-mail:',
        }

        widgets = {
            'username': forms.NumberInput(attrs={'class':'input_cad', 'placeholder': 'Digite a matrícula do ADMIN:'}),
            'first_name': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome do ADMIN:'}),
            'email': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite o e-mail do ADMIN:'}),
        }
    

# --------------------------------------------------------------------------------------------------------------------------

# formulario de perfil Admin

class perfilAdminForm(forms.ModelForm):
    class Meta:
        model = PerfilAdmin
        exclude = ['usuario']
        labels = {
            'foto_perfil':'Foto de perfil:',
        }

        widgets = {
            'foto_perfil': forms.FileInput(attrs={'class':'img_edit'})
        }


class senhaAdminForms(forms.Form):
    # Senha
    senha=forms.CharField(
        label="Senha:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_cad',
                'placeholder': 'Digite sua senha:'
            }
        )
    )

    # Confirmar senha
    confirmar_senha=forms.CharField(
        label="Confirme a senha:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_cad',
                'placeholder': 'Repita a senha digitada acima:'
            }
        )
    )

# --------------------------------------------------------------------------------------------------------------------------

# formularios de cadastro de Instituições

class instituicaoForms(forms.ModelForm):
    class Meta:
        model = Instituicao
        exclude = ['criador']
        labels = {
            'nome_instituicao':'Nome:',
            'sigla':'Sigla:',
            'estado':'Estado:',
        }

        widgets = {
            'nome_instituicao': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome da instituição:'}),
            'sigla': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite a sigla da instituição:'}),
            'estado': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o estado da instituição:'}),
        }

# --------------------------------------------------------------------------------------------------------------------------

# formularios de cadastro de cursos

class cursoForms(forms.ModelForm):
    class Meta:
        model = Curso
        exclude = ['criador']
        labels = {
            'nome_curso':'Nome:',
            'descricao_curso':'Descrição:',
        }

        widgets = {
            'nome_curso': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome do Curso:'}),
            'descricao_curso': forms.Textarea(attrs={'class':'descr_input', 'placeholder': 'Digite a descrição do Curso:'}),
        }

# --------------------------------------------------------------------------------------------------------------------------

# formularios de cadastro de campus

class campusForms(forms.ModelForm):
    class Meta:
        model = Campus
        exclude = ['criador']
        labels = {
            'nome_campus':'Nome:',
            'email_campus':'Email:',
            'endereco_campus':'Endereço:',
            'cidade_campus':'Cidade:',
            'instituicao_campus':'Instituição:',
            'cursos_campus':'Cursos:',
        }

        widgets = {
            'nome_campus': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome do Campus:'}),
            'email_campus': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite o email do Campus:'}),
            'endereco_campus': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o endereço do Campus:'}),
            'cidade_campus': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite a cidade do Campus:'}),
            'instituicao_campus': forms.Select(attrs={'class':'input_cad', 'placeholder': 'selecione a instituição que o Campus pertence:'}),
            'cursos_campus': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instituicao_campus'].empty_label = "Selecione a instituição que o campus pertence"

# --------------------------------------------------------------------------------------------------------------------------

# formularios de cadastro de categoria

class categoriaForms(forms.ModelForm):
    class Meta:
        model = Categoria
        exclude = ['criador']
        labels = {
            'nome_categoria':'Nome:',
            'descricao_categoria':'Descrição:',
        }

        widgets = {
            'nome_categoria': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome da Categoria:'}),
            'descricao_categoria': forms.Textarea(attrs={'class':'descr_input', 'placeholder': 'Digite a descrição da Categoria:'}),
        }

# --------------------------------------------------------------------------------------------------------------------------

# formularios de cadastro de tipo

class tipoForms(forms.ModelForm):
    class Meta:
        model = Tipos
        exclude = ['criador']
        labels = {
            'nome_tipo':'Nome:',
            'descricao_tipo':'Descrição:',
        }

        widgets = {
            'nome_tipo': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome do Tipo de conteudo:'}),
            'descricao_tipo': forms.Textarea(attrs={'class':'descr_input', 'placeholder': 'Digite a descrição do Tipo de conteudo:'}),
        }

# --------------------------------------------------------------------------------------------------------------------------

# formularios bibliotecario

# formularios de cadastro de usuario bibliotecario
class cadastroBibliotecarioForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

        labels = {
            'username':'Matrícula:',
            'first_name':'Nome:',
            'email':'E-mail:',
        }

        widgets = {
            'username': forms.NumberInput(attrs={'class':'input_cad', 'placeholder': 'Digite a matrícula do Bibliotecario:'}),
            'first_name': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome do Bibliotecario:'}),
            'email': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite o e-mail do Bibliotecario:'}),
        }
    
# formularios de cadastro de perfil de bibliotecario
class perfilBibliotecarioForms(forms.ModelForm):
    class Meta:
        model = PerfilBibliotecario
        exclude = ['usuario', 'tipo_user', 'foto_perfil', 'criador', 'instituicao']

        labels = {
            'campus':'Campus:',
        }

        widgets = {
            'campus': forms.Select(attrs={'class':'input_cad'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campus'].empty_label = "Selecione o campus que o bibliotecário irá gerenciar"