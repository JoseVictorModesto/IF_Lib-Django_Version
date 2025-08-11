from django import forms

from django.contrib.auth.models import User

from apps.user_bibliotecario.models import PerfilAluno

# formulario Perfil Aluno

# formularios de editar informacoes do aluno
class editarUserAluno(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

        labels = {
            'email':'E-mail:',
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite seu e-mail:'})
        }

class editarPerfilAlunoForms(forms.ModelForm):
    class Meta:
        model = PerfilAluno
        fields = ['curso']

        labels = {
            'curso':'Curso:',
        }

        widgets = {
            'curso': forms.Select(attrs={'class':'input_cad'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].empty_label = "Selecione um curso:"

# formulario de editar foto de perfil do aluno
class fotoAlunoForms(forms.ModelForm):
    class Meta:
        model = PerfilAluno
        fields = ['foto_perfil']

        labels = {
            'foto_perfil':'Foto de perfil:',
        }

        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={'class':'img_edit'}),
        }

# --------------------------------------------------------------------------------------------------------------------------