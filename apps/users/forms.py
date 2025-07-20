from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import User


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        label='Nome completo',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome completo'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@cepuerj.uerj.br'})
    )
    department = forms.CharField(
        label='Departamento',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Seu departamento'})
    )
    position = forms.CharField(
        label='Cargo',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Seu cargo'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'department', 'position', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h3 class="text-2xl font-bold text-gray-900 mb-6 text-center">Criar Conta na Trilha Gamificada</h3>'),
            Row(
                Column('username', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'full_name',
            Row(
                Column('department', css_class='form-group col-md-6 mb-3'),
                Column('position', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-3'),
                Column('password2', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            HTML('<div class="text-center mt-4">'),
            Submit('submit', 'Começar Minha Jornada', css_class='btn btn-primary btn-lg px-5 py-3 rounded-pill'),
            HTML('</div>'),
        )
        
        # Customize field widgets
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg rounded-pill'
            })


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'department', 'position', 'avatar', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('department', css_class='form-group col-md-6 mb-3'),
                Column('position', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'avatar',
            'bio',
            Submit('submit', 'Atualizar Perfil', css_class='btn btn-primary')
        )