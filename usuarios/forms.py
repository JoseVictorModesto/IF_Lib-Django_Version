from django import forms
from usuarios.models import PerfilAdmin

#formularios de login

class LoginForms(forms.Form):
# email
    matricula_login = forms.IntegerField(
        label="Matrícula:",
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'input_form_login',
                'placeholder': 'informe seu número de matrícula:'
            }
        )
    )

#senha
    senha_login=forms.CharField(
        label="Senha:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_form_login',
                'placeholder': 'Digite sua senha:'
            }
        )
    )

# --------------------------------------------------------------------------------------------------------------------------

# formulario de cadastro Admin   

class cadastroAdminForms(forms.Form):

    # matricula do admin
    matricula_admin=forms.IntegerField(
        label="Matrícula:",
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'input_cad',
                'placeholder': 'Digite o número de matrícula do Admin:'
            }
        )
    )

    # nome do admin
    nome_admin=forms.CharField(
        label="Nome:",
        required=True,
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'input_cad',
                'placeholder': 'Digite o nome do Admin:'
            }
        )
    )
    
    # email do admin
    email_admin=forms.EmailField(
        label="E-mail:",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'input_cad',
                'placeholder': 'Digite o e-mail do Admin:'
            }
        )
    )

    # senha do admin
    senha_admin=forms.CharField(
        label="Senha:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_cad',
                'placeholder': 'Digite uma senha:'
            }
        )
    )

    confirmar_senha_admin=forms.CharField(
        label="Confirme a Senha:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input_cad',
                'placeholder': 'Digite a senha novamente:'
            }
        )
    ) 

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