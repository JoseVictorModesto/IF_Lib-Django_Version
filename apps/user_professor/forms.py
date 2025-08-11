from django import forms

from django.contrib.auth.models import User

from apps.user_bibliotecario.models import PerfilProfessor


# formularios Perfil Professor

# formularios de editar informacoes do professor
class editarUserProfessorForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

        labels = {
            'email':'E-mail:',
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class':'input_cad', 'placeholder': 'Digite seu e-mail:'})
        }

class editarPerfilProfessorForms(forms.ModelForm):
    class Meta:
        model = PerfilProfessor
        fields = ['formacao']

        labels = {
            'formacao':'Formação:',
        }

        widgets = {
            'formacao': forms.TextInput(attrs={'class':'input_cad', 'placeholder': 'Digite sua formação:'}),
        }

# formulario de editar foto de perfil do professor
class fotoProfessorForms(forms.ModelForm):
    class Meta:
        model = PerfilProfessor
        fields = ['foto_perfil']

        labels = {
            'foto_perfil':'Foto de perfil:',
        }

        widgets = {
            'foto_perfil': forms.FileInput(attrs={'class':'img_edit'}),
        }

# --------------------------------------------------------------------------------------------------------------------------
