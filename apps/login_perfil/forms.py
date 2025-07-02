from django import forms

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

# formularios de redefinir a senha do usuario
class senhaUsuarioForms(forms.Form):
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