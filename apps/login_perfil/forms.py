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