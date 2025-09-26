import os
import logging
from django.conf import settings
from google import genai
from google.genai import types
from .models import ProvedorIA

logger = logging.getLogger(__name__)

def get_gemini_client():
    """Obtém cliente Gemini configurado"""
    try:
        # Buscar provedor Gemini ativo
        provedor = ProvedorIA.objects.filter(
            nome__icontains="gemini",
            ativo=True
        ).first()
        
        if not provedor:
            raise ValueError("Nenhum provedor Gemini ativo encontrado. Configure um provedor de IA.")
        
        if not provedor.api_key:
            raise ValueError("Chave da API não configurada no provedor Gemini.")
        
        return genai.Client(api_key=provedor.api_key)
        
    except Exception as e:
        logger.error(f"Erro ao configurar cliente Gemini: {str(e)}")
        raise ValueError(f"Erro ao configurar cliente Gemini: {str(e)}")

def analyze_oct_image(image_path):
    """
    Analisa uma imagem OCT usando Gemini AI e retorna o diagnóstico
    """
    try:
        # Buscar provedor Gemini ativo
        provedor = ProvedorIA.objects.filter(
            nome__icontains="gemini",
            ativo=True
        ).first()
        
        if not provedor:
            return {
                'success': False,
                'diagnostico': None,
                'error': 'Nenhum provedor Gemini ativo encontrado. Configure um provedor de IA.'
            }
        
        # Template de prompt específico para análise OCT
        prompt_template = """
        Como especialista em Retina e Vítreo com expertise em Tomografia de Coerência Óptica, analise esta imagem de OCT macular e forneça um laudo estruturado, objetivo e técnico.

        ESTRUTURE O LAUDO CONFORME MODELO:

        ## ANÁLISE TÉCNICA DA IMAGEM OCT

        ### QUALIDADE DA IMAGEM
        - Avalie a qualidade técnica (boa/regular/limitada)
        - Centralização foveal
        - Presença de artefatos

        ### ANATOMIA RETINIANA
        **Camadas Retinianas:**
        - Membrana limitante interna
        - Camadas plexiformes e nucleares
        - Zona elipsoide e membrana limitante externa
        - Epitélio pigmentar da retina (EPR)
        - Complexo EPR/Membrana de Bruch

        **Morfologia Foveal:**
        - Depressão foveal (presente/ausente/alterada)
        - Espessura foveal estimada
        - Arquitetura das camadas externas

        ### ACHADOS PATOLÓGICOS
        **Alterações Intraretinianas:**
        - Edema cistoide (ausente/leve/moderado/severo)
        - Espessamento retiniano
        - Desorganização das camadas (DRIL)

        **Alterações Sub-retinianas:**
        - Fluido sub-retiniano
        - Descolamento neurossensorial
        - Material sub-retiniano

        **Alterações do EPR:**
        - Descolamento do EPR
        - Elevações drusenóides
        - Atrofia do EPR

        ### DIAGNÓSTICO DIFERENCIAL
        1. **Hipótese Principal:** [Diagnóstico mais provável]
        2. **Diagnósticos Diferenciais:** [Até 2 alternativas]
        3. **Classificação:** [Grau/Estágio se aplicável]

        ### RECOMENDAÇÕES CLÍNICAS
        - Seguimento oftalmológico
        - Exames complementares indicados
        - Conduta terapêutica sugerida

        IMPORTANTE: Use terminologia médica precisa, seja conciso e evite expressões coloquiais como "com certeza". Mantenha tom profissional e científico.
        """
        
        # Ler a imagem
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        # Obter cliente Gemini
        client = get_gemini_client()
        
        # Enviar para Gemini AI
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                prompt_template
            ],
        )
        
        if response.text:
            logger.info(f"Análise OCT realizada com sucesso para imagem: {image_path}")
            return {
                'success': True,
                'diagnostico': response.text,
                'error': None,
                'provedor_usado': provedor.nome
            }
        else:
            logger.error(f"Resposta vazia da API Gemini para imagem: {image_path}")
            return {
                'success': False,
                'diagnostico': None,
                'error': 'Resposta vazia da API de IA'
            }
            
    except Exception as e:
        logger.error(f"Erro ao analisar imagem OCT {image_path}: {str(e)}")
        return {
            'success': False,
            'diagnostico': None,
            'error': f'Erro na análise: {str(e)}'
        }

def create_oct_prompt(prompt_text=None):
    """
    Cria um prompt personalizado para análise OCT
    """
    if prompt_text:
        return prompt_text
    
    # Prompt padrão se nenhum for fornecido
    return """
    Analise esta imagem de OCT (Tomografia de Coerência Óptica) e forneça:
    
    1. Descrição anatômica das estruturas visíveis
    2. Identificação de alterações patológicas
    3. Diagnóstico provável
    4. Recomendações clínicas
    
    Forneça um laudo médico profissional detalhado.
    """