from django import forms
from apps.user_admin.models import User, PerfilAdmin, Instituicao, Curso, Campus, Categoria, Tipos

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
                'class': 'input_form_login',
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
                'class': 'input_form_login',
                'placeholder': 'Repita a senha digitada acima sua senha:'
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
            'descricao_curso': forms.Textarea(attrs={'class':'input_cad', 'placeholder': 'Digite a descrição do Curso:'}),
        }

# formularios de cadastro de cursos

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
            'descricao_categoria': forms.Textarea(attrs={'class':'input_cad', 'placeholder': 'Digite a descrição da Categoria:'}),
        }

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
            'descricao_tipo': forms.Textarea(attrs={'class':'input_cad', 'placeholder': 'Digite a descrição do Tipo de conteudo:'}),
        }