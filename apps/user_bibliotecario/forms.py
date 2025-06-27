from django import forms

from django.contrib.auth.models import User

from apps.user_admin.models import PerfilBibliotecario
from apps.user_bibliotecario.models import PerfilProfessor, PerfilAluno

# formularios Perfil bibliotecario

# formularios de editar perfil informacoes do bibliotecario
class editarBibliotecarioForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

        labels = {
            'email':'E-mail:',
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite o e-mail do Bibliotecario:'}),
        }
    
# formularios de editar a foto de perfil do bibliotecario
class fotoBibliotecarioForms(forms.ModelForm):
    class Meta:
        model = PerfilBibliotecario
        fields = ['foto_perfil']

        labels = {
            'foto_perfil':'Foto de perfil:',
        }

        widgets = {
            'foto_perfil': forms.FileInput(attrs={'class':'img_edit'}),
        }

# formularios de redefinir a senha do bibliotecario
class senhaBibliotecarioForms(forms.Form):
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

# formularios professores

# formularios de cadastro do usuario professor
class cadastroProfessorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

        labels = {
            'username':'Matrícula:',
            'first_name':'Nome:',
            'email':'E-mail:',
            }
        
        widgets = {
            'username': forms.NumberInput(attrs={'class':'input_cad', 'placeholder': 'Digite a matrícula do Professor:'}),
            'first_name': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome do Professor:'}),
            'email': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite o e-mail do Professor:'}),
            }

# formularios de cadastro do perfil professor
class perfilProfessorForm(forms.ModelForm):
    class Meta:
        model = PerfilProfessor
        exclude = ['usuario', 'tipo_user', 'instituicao', 'foto_perfil', 'criador', 'campus']

        labels = {
            'formacao':'Formação:',
        }

        widgets = {
            'formacao': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite a formação do Professor:'}),
        }

# formularios de editar professor
class editarProfessorForm(forms.ModelForm):
    class Meta:
        model = PerfilProfessor
        exclude = ['usuario', 'tipo_user', 'instituicao', 'foto_perfil', 'criador']

        labels = {
            'formacao':'Formação:',
            'campus':'Campus:',
        }

        widgets = {
            'formacao': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite a formação do Professor:'}),
            'campus': forms.Select(attrs={'class':'input_cad'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campus'].empty_label = "Selecione um campus:"

# --------------------------------------------------------------------------------------------------------------------------

# formularios alunos

# formularios de cadastro do usuario aluno
class cadastroAlunoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

        labels = {
            'username':'Matrícula:',
            'first_name':'Nome:',
            'email':'E-mail:',
            }
        
        widgets = {
            'username': forms.NumberInput(attrs={'class':'input_cad', 'placeholder': 'Digite a matrícula do Aluno:'}),
            'first_name': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite o nome do Aluno:'}),
            'email': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite o e-mail do Aluno:'}),
        }

# formularios de cadastro do usuario aluno
class perfilAlunoForm(forms.ModelForm):
    class Meta:
        model = PerfilAluno
        exclude = ['usuario', 'tipo_user', 'instituicao', 'foto_perfil', 'criador', 'campus']

        labels = {
            'curso':'Curso:',
        }

        widgets = {
            'curso': forms.Select(attrs={'class':'input_cad'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].empty_label = "Selecione um curso:"

# formularios de editar aluno
class editarAlunoForm(forms.ModelForm):
    class Meta:
        model = PerfilAluno
        exclude = ['usuario', 'tipo_user', 'instituicao', 'foto_perfil', 'criador']

        labels = {
            'campus':'Campus:',
            'curso':'Curso:',
        }

        widgets = {
            'campus': forms.Select(attrs={'class':'input_cad'}),
            'curso': forms.Select(attrs={'class':'input_cad'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campus'].empty_label = "Selecione um campus:"
        self.fields['curso'].empty_label = "Selecione um curso:"