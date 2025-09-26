from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import Paciente, ExameOCT, ProvedorIA, PromptIA
from .forms import CustomUserCreationForm, PacienteForm, ExameOCTForm
from .ai_service import analyze_oct_image
from .pdf_service import gerar_laudo_pdf
from django.http import FileResponse
from django.core.files.base import ContentFile

@login_required
def home(request):
    """Página inicial do sistema"""
    exames_recentes = ExameOCT.objects.filter(usuario=request.user).order_by('-data_exame')[:5]
    pacientes_count = Paciente.objects.count()
    exames_count = ExameOCT.objects.count()

    context = {
        'exames_recentes': exames_recentes,
        'pacientes_count': pacientes_count,
        'exames_count': exames_count,
    }
    return render(request, 'core/home.html', context)

def register(request):
    """Registro de novos usuários"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def paciente_list(request):
    """Lista de pacientes"""
    pacientes = Paciente.objects.all().order_by('nome')
    return render(request, 'core/paciente_list.html', {'pacientes': pacientes})

@login_required
def paciente_create(request):
    """Criar novo paciente"""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('paciente_list')
    else:
        form = PacienteForm()
    return render(request, 'core/paciente_form.html', {'form': form, 'title': 'Novo Paciente'})

@login_required
def exame_create(request):
    """Criar novo exame OCT"""
    if request.method == 'POST':
        form = ExameOCTForm(request.POST, request.FILES)
        if form.is_valid():
            exame = form.save(commit=False)
            exame.usuario = request.user
            exame.save()
            messages.success(request, 'Exame OCT enviado com sucesso!')
            return redirect('exame_analyze', exame.id)
    else:
        form = ExameOCTForm()
    return render(request, 'core/exame_form.html', {'form': form, 'title': 'Novo Exame OCT'})

@login_required
def exame_analyze(request, exame_id):
    """Página de análise do exame"""
    exame = get_object_or_404(ExameOCT, id=exame_id)
    return render(request, 'core/exame_analyze.html', {'exame': exame})

@login_required
def exame_analyze_ai(request, exame_id):
    """Processa análise de IA para um exame OCT"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    exame = get_object_or_404(ExameOCT, id=exame_id)

    # Verificar se o usuário pode analisar este exame
    if exame.usuario != request.user:
        return JsonResponse({'error': 'Sem permissão para analisar este exame'}, status=403)

    # Verificar se já foi analisado
    if exame.diagnostico_ia:
        return JsonResponse({'error': 'Este exame já foi analisado'}, status=400)

    try:
        # Atualizar status para "analisando"
        exame.status = 'analisando'
        exame.save()

        # Obter caminho da imagem
        image_path = exame.imagem.path

        # Verificar se o arquivo existe
        if not os.path.exists(image_path):
            exame.status = 'erro'
            exame.save()
            return JsonResponse({'error': 'Arquivo de imagem não encontrado'}, status=404)

        # Buscar provedor Gemini ativo para salvar no exame
        provedor = ProvedorIA.objects.filter(
            nome__icontains="gemini",
            ativo=True
        ).first()

        # Analisar com IA
        resultado = analyze_oct_image(image_path)

        if resultado['success']:
            # Salvar resultado
            exame.diagnostico_ia = resultado['diagnostico']
            exame.data_diagnostico = timezone.now()
            exame.status = 'concluido'
            exame.provedor_ia = provedor
            exame.save()

            return JsonResponse({
                'success': True,
                'diagnostico': resultado['diagnostico'],
                'data_diagnostico': exame.data_diagnostico.strftime('%d/%m/%Y %H:%M')
            })
        else:
            # Erro na análise
            exame.status = 'erro'
            exame.save()
            return JsonResponse({
                'success': False,
                'error': resultado['error'] or 'Erro desconhecido na análise'
            })

    except Exception as e:
        # Erro inesperado
        exame.status = 'erro'
        exame.save()
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        })

@login_required
def gerar_laudo_pdf_view(request, exame_id):
    """Gera e retorna o laudo PDF de um exame"""
    exame = get_object_or_404(ExameOCT, id=exame_id)

    # Verificar se o usuário pode acessar este exame
    if exame.usuario != request.user:
        return JsonResponse({'error': 'Sem permissão para acessar este exame'}, status=403)

    # Verificar se o exame tem diagnóstico
    if not exame.diagnostico_ia:
        return JsonResponse({'error': 'Exame ainda não foi analisado'}, status=400)

    try:
        # Gerar PDF
        pdf_buffer = gerar_laudo_pdf(exame)

        # Salvar PDF no modelo
        filename = f"laudo_{exame.paciente.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        exame.laudo_pdf.save(
            filename,
            ContentFile(pdf_buffer.getvalue()),
            save=True
        )
        exame.data_laudo = timezone.now()
        exame.save()

        # Retornar o PDF
        pdf_buffer.seek(0)
        response = FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=filename,
            content_type='application/pdf'
        )
        return response

    except Exception as e:
        return JsonResponse({'error': f'Erro ao gerar PDF: {str(e)}'}, status=500)

@login_required
def check_gemini_key(request):
    """Verifica se a chave Gemini está configurada"""
    from .models import ProvedorIA

    provedor = ProvedorIA.objects.filter(
        nome__icontains="gemini",
        ativo=True
    ).first()

    return JsonResponse({
        'key_configured': bool(provedor and provedor.api_key)
    })