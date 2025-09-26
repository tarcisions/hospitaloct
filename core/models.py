from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

# Model para Pacientes
class Paciente(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Paciente")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    prontuario = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prontuário")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.prontuario or 'S/N'}"

# Model para Provedores de IA (Gemini, OpenAI, DeepSeek, etc.)
class ProvedorIA(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Provedor")
    api_url = models.URLField(verbose_name="URL da API")
    api_key = models.CharField(max_length=500, verbose_name="Chave da API")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Provedor de IA"
        verbose_name_plural = "Provedores de IA"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

# Model para Prompts configuráveis para cada IA
class PromptIA(models.Model):
    provedor = models.ForeignKey(ProvedorIA, on_delete=models.CASCADE, verbose_name="Provedor de IA")
    nome = models.CharField(max_length=100, verbose_name="Nome do Prompt")
    prompt_template = models.TextField(verbose_name="Template do Prompt")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Prompt de IA"
        verbose_name_plural = "Prompts de IA"
        ordering = ['provedor', 'nome']
    
    def __str__(self):
        return f"{self.provedor.nome} - {self.nome}"

# Função para upload de imagens OCT
def upload_to_oct(instance, filename):
    """Define o caminho para upload das imagens OCT"""
    ext = filename.split('.')[-1]
    filename = f"oct_{instance.paciente.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('exames_oct', filename)

# Função para upload de laudos PDF
def upload_to_laudos(instance, filename):
    """Define o caminho para upload dos laudos PDF"""
    filename = f"laudo_{instance.paciente.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return os.path.join('laudos_pdf', filename)

# Model para Exames OCT
class ExameOCT(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário que realizou o upload")
    imagem = models.ImageField(upload_to=upload_to_oct, verbose_name="Imagem OCT")
    data_exame = models.DateTimeField(auto_now_add=True, verbose_name="Data do Exame")
    
    # Dados do diagnóstico
    provedor_ia = models.ForeignKey(ProvedorIA, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Provedor de IA")
    prompt_usado = models.ForeignKey(PromptIA, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Prompt Utilizado")
    diagnostico_ia = models.TextField(blank=True, null=True, verbose_name="Diagnóstico da IA")
    data_diagnostico = models.DateTimeField(null=True, blank=True, verbose_name="Data do Diagnóstico")
    
    # Laudo final
    laudo_pdf = models.FileField(upload_to=upload_to_laudos, null=True, blank=True, verbose_name="Laudo PDF")
    data_laudo = models.DateTimeField(null=True, blank=True, verbose_name="Data do Laudo")
    
    # Status do exame
    STATUS_CHOICES = [
        ('pendente', 'Pendente de Análise'),
        ('analisando', 'Analisando'),
        ('concluido', 'Concluído'),
        ('erro', 'Erro na Análise'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    
    class Meta:
        verbose_name = "Exame OCT"
        verbose_name_plural = "Exames OCT"
        ordering = ['-data_exame']
    
    def __str__(self):
        return f"OCT - {self.paciente.nome} - {self.data_exame.strftime('%d/%m/%Y')}"
    
    @property
    def tem_diagnostico(self):
        """Verifica se o exame já tem diagnóstico"""
        return bool(self.diagnostico_ia)
    
    @property
    def tem_laudo(self):
        """Verifica se o exame já tem laudo PDF"""
        return bool(self.laudo_pdf)