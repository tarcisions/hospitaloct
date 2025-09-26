from django.contrib import admin
from .models import Paciente, ProvedorIA, PromptIA, ExameOCT

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_nascimento', 'prontuario', 'criado_em']
    list_filter = ['criado_em', 'data_nascimento']
    search_fields = ['nome', 'prontuario']
    ordering = ['nome']

@admin.register(ProvedorIA)
class ProvedorIAAdmin(admin.ModelAdmin):
    list_display = ['nome', 'api_url', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome']
    list_editable = ['ativo']

@admin.register(PromptIA)
class PromptIAAdmin(admin.ModelAdmin):
    list_display = ['nome', 'provedor', 'ativo', 'criado_em']
    list_filter = ['provedor', 'ativo', 'criado_em']
    search_fields = ['nome', 'provedor__nome']
    list_editable = ['ativo']

@admin.register(ExameOCT)
class ExameOCTAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'usuario', 'data_exame', 'status']
    list_filter = ['status', 'data_exame', 'provedor_ia']
    search_fields = ['paciente__nome', 'usuario__username']
    readonly_fields = ['data_exame', 'data_diagnostico', 'data_laudo']
    ordering = ['-data_exame']
