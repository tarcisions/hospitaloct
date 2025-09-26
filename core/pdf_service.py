
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from django.conf import settings
from django.utils import timezone
import os
import io

def gerar_laudo_pdf(exame):
    """
    Gera um laudo PDF profissional para um exame OCT
    """
    # Criar buffer para o PDF
    buffer = io.BytesIO()
    
    # Criar documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para o título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor='#2C3E50'
    )
    
    # Estilo para seções
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor='#34495E',
        leftIndent=0
    )
    
    # Estilo para conteúdo
    content_style = ParagraphStyle(
        'ContentText',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leftIndent=10
    )
    
    # Estilo para dados do paciente
    data_style = ParagraphStyle(
        'DataText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leftIndent=10
    )
    
    # Construir conteúdo do PDF
    story = []
    
    # Cabeçalho
    story.append(Paragraph("LAUDO DE TOMOGRAFIA DE COERÊNCIA ÓPTICA (OCT)", title_style))
    story.append(Spacer(1, 20))
    
    # Dados do Paciente
    story.append(Paragraph("DADOS DO PACIENTE", section_style))
    story.append(Paragraph(f"<b>Nome:</b> {exame.paciente.nome}", data_style))
    story.append(Paragraph(f"<b>Data de Nascimento:</b> {exame.paciente.data_nascimento.strftime('%d/%m/%Y')}", data_style))
    if exame.paciente.prontuario:
        story.append(Paragraph(f"<b>Prontuário:</b> {exame.paciente.prontuario}", data_style))
    story.append(Paragraph(f"<b>Data do Exame:</b> {exame.data_exame.strftime('%d/%m/%Y às %H:%M')}", data_style))
    if exame.data_diagnostico:
        story.append(Paragraph(f"<b>Data da Análise:</b> {exame.data_diagnostico.strftime('%d/%m/%Y às %H:%M')}", data_style))
    if exame.provedor_ia:
        story.append(Paragraph(f"<b>Sistema de Análise:</b> {exame.provedor_ia.nome}", data_style))
    story.append(Spacer(1, 20))
    
    # Diagnóstico por IA
    if exame.diagnostico_ia:
        story.append(Paragraph("ANÁLISE POR INTELIGÊNCIA ARTIFICIAL", section_style))
        
        # Processar o diagnóstico para melhor formatação
        diagnostico_formatado = processar_diagnostico_para_pdf(exame.diagnostico_ia)
        
        for paragrafo in diagnostico_formatado:
            story.append(Paragraph(paragrafo, content_style))
            story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 30))
    
    # Rodapé
    story.append(Paragraph("IMPORTANTE", section_style))
    story.append(Paragraph(
        "Este laudo foi gerado por sistema de inteligência artificial e deve ser "
        "revisado por um médico especialista. Não substitui a avaliação clínica "
        "profissional e a correlação com o quadro clínico do paciente.",
        content_style
    ))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Laudo gerado em: {timezone.now().strftime('%d/%m/%Y às %H:%M')}", data_style))
    
    # Construir PDF
    doc.build(story)
    
    # Retornar buffer
    buffer.seek(0)
    return buffer

def processar_diagnostico_para_pdf(diagnostico_texto):
    """
    Processa o texto do diagnóstico para melhor formatação no PDF
    """
    linhas = diagnostico_texto.split('\n')
    paragrafos_formatados = []
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        # Títulos com asteriscos ou hashes
        if linha.startswith('###') or linha.startswith('**') or linha.startswith('####'):
            linha_limpa = linha.replace('#', '').replace('*', '').strip()
            if linha_limpa:
                paragrafos_formatados.append(f"<b>{linha_limpa}</b>")
        # Listas com asteriscos ou hífens
        elif linha.startswith('* ') or linha.startswith('- '):
            item = linha[2:].strip()
            paragrafos_formatados.append(f"• {item}")
        # Texto normal
        elif linha and not linha.startswith('---'):
            paragrafos_formatados.append(linha)
    
    return paragrafos_formatados
