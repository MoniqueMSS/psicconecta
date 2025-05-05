from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    idade = forms.IntegerField(label="Idade")
    genero = forms.CharField(label="Gênero", max_length=50)
    email = forms.EmailField(label="Email")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'idade', 'genero')
        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.',
        }
        error_messages = {
            'username': {
                'required': 'Por favor, digite um nome de usuário.',
                'max_length': 'O nome de usuário não pode ter mais de 150 caracteres.',
                'invalid': 'Digite um nome de usuário válido. Este valor pode conter apenas letras, números e @/./+/-/_.'
            },
            'email': {
                'required': 'Por favor, digite um endereço de email.',
                'invalid': 'Digite um endereço de email válido.',
            },
            'password': {
                'password_too_short': 'Sua senha deve ter no mínimo %(min_length)d caracteres.',
                'password_too_similar': 'Sua senha é muito similar às suas outras informações pessoais.',
                'password_common_usage': 'Esta é uma senha muito comum.',
                'password_entirely_numeric': 'Sua senha não pode ser inteiramente numérica.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de Usuário"
        self.fields['email'].label = "Email"
        self.fields['idade'].label = "Idade"
        self.fields['genero'].label = "Gênero"
        # O label da senha é definido na classe base UserCreationForm


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput,
        required=True,
        min_length=8,  # Mínimo de 8 caracteres
        error_messages={'min_length': "A senha deve ter pelo menos 8 caracteres."}
    )
    confirm_password = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput,
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data