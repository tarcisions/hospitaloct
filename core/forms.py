from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Paciente, ExameOCT

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=30, required=True, label="Sobrenome")
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'prontuario']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do paciente'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prontuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do prontuário (opcional)'}),
        }

class ExameOCTForm(forms.ModelForm):
    class Meta:
        model = ExameOCT
        fields = ['paciente', 'imagem']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }