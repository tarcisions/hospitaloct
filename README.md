
# 🔬 Sistema OCT Premium

Sistema completo para análise de exames de Tomografia de Coerência Óptica (OCT) utilizando Inteligência Artificial.

## 🚀 Funcionalidades

- 👥 **Gerenciamento de Pacientes**: Cadastro e listagem de pacientes
- 📷 **Upload de Exames OCT**: Interface intuitiva para envio de imagens
- 🤖 **Análise por IA**: Diagnóstico automático usando Google Gemini AI
- 📄 **Geração de Laudos PDF**: Relatórios profissionais em PDF
- 🎨 **Interface Profissional**: Design moderno e responsivo estilo office
- 🔐 **Sistema de Autenticação**: Login seguro com diferentes níveis de acesso

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5 + CSS Premium customizado
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **IA**: Google Gemini AI
- **PDF**: ReportLab
- **Imagens**: Pillow

## 📋 Pré-requisitos

- Python 3.11+
- pip (gerenciador de pacotes Python)
- Chave API do Google Gemini AI

## 🔧 Instalação Local

### 1. Clone o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd sistema-oct-premium
```

### 2. Crie e ative um ambiente virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install django==5.2.6
pip install google-genai==1.38.0
pip install pillow==11.3.0
pip install python-decouple==3.8
pip install reportlab==4.4.3
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
# Chave da API do Google Gemini
GEMINI_API_KEY=sua_chave_aqui

# Configurações do Django
SECRET_KEY=django-insecure-sua-chave-secreta-aqui
DEBUG=True

# Configurações de banco (opcional - padrão SQLite)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 5. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Colete arquivos estáticos (se necessário)
```bash
python manage.py collectstatic --noinput
```

### 8. Execute o servidor
```bash
python manage.py runserver 0.0.0.0:5000
```

### 9. Acesse o sistema
- **Sistema**: http://localhost:5000
- **Admin**: http://localhost:5000/admin

## 🌐 Deploy no Replit

### 1. Importar Projeto
1. Acesse https://replit.com
2. Clique em "Import from GitHub"
3. Cole a URL do repositório
4. Clique em "Import"

### 2. Configurar Variáveis de Ambiente
1. No painel lateral, clique no ícone de "Secrets" (🔒)
2. Adicione a seguinte variável:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Sua chave da API do Google Gemini

### 3. Executar o Projeto
1. Clique no botão "Run"
2. O projeto será iniciado automaticamente em `https://seu-projeto.replit.app`

### 4. Configurar Provedor de IA
1. Acesse o painel admin: `https://seu-projeto.replit.app/admin`
2. Faça login com o superusuário
3. Vá em "Provedores de IA" e clique em "Adicionar"
4. Configure:
   - **Nome**: `Gemini AI`
   - **API URL**: `https://generativelanguage.googleapis.com`
   - **API Key**: Sua chave do Gemini
   - **Ativo**: ✅ Marcado

## 🔑 Obtendo Chave da API do Google Gemini

### 1. Acesse o Google AI Studio
- Vá para: https://makersuite.google.com/app/apikey

### 2. Crie uma nova chave
1. Clique em "Create API Key"
2. Selecione um projeto do Google Cloud (ou crie um novo)
3. Copie a chave gerada

### 3. Configure no sistema
- **Arquivo .env**: `GEMINI_API_KEY=sua_chave_aqui`
- **Replit**: Adicione em Secrets como `GEMINI_API_KEY`

## 🎨 Personalizando o Prompt da IA

### 1. Via Painel Admin
1. Acesse `/admin` do seu sistema
2. Vá em "Prompts de IA"
3. Clique em "Adicionar prompt IA"
4. Configure:
   - **Provedor**: Selecione o Gemini AI configurado
   - **Nome**: Nome descritivo do prompt
   - **Template do Prompt**: Seu prompt personalizado
   - **Ativo**: ✅ Marcado

### 2. Editando no Código
Edite o arquivo `core/ai_service.py` na função `analyze_oct_image()`:

```python
# Localize esta seção no código (linha ~45):
prompt_template = """
Você é um especialista em análise de imagens de OCT...
[SEU PROMPT PERSONALIZADO AQUI]
"""
```

### 3. Exemplo de Prompt Personalizado
```
Você é um oftalmologista especialista em OCT com 20 anos de experiência. 
Analise esta imagem de Tomografia de Coerência Óptica e forneça:

**LAUDO MÉDICO ESTRUTURADO:**

1. **DADOS TÉCNICOS:**
   - Qualidade da imagem (boa/regular/ruim)
   - Centralização da fóvea
   - Presença de artefatos

2. **ACHADOS ANATÔMICOS:**
   - Espessura foveal central (em μm, se possível estimar)
   - Integridade das camadas retinianas
   - Estado do epitélio pigmentar da retina (EPR)
   - Presença de fluidos (intraretiniano/subretiniano)

3. **DIAGNÓSTICO DIFERENCIAL:**
   - Patologia principal identificada
   - Diagnósticos diferenciais possíveis
   - Grau de severidade (leve/moderado/severo)

4. **RECOMENDAÇÕES CLÍNICAS:**
   - Seguimento recomendado
   - Exames complementares necessários
   - Tratamento sugerido

Use terminologia médica precisa e seja objetivo no diagnóstico.
```

## 📁 Estrutura do Projeto

```
sistema-oct-premium/
├── core/                      # App principal Django
│   ├── migrations/           # Migrações do banco de dados
│   ├── templates/           # Templates HTML
│   │   ├── core/           # Templates do core
│   │   └── registration/   # Templates de login/registro
│   ├── ai_service.py        # Serviço de integração com IA
│   ├── pdf_service.py       # Geração de laudos PDF
│   ├── models.py            # Modelos do banco de dados
│   ├── views.py             # Views do Django
│   ├── forms.py             # Formulários
│   ├── urls.py              # URLs do app
│   └── admin.py             # Configuração do admin
├── static/                   # Arquivos estáticos
│   └── css/
│       └── style.css        # CSS premium customizado
├── media/                    # Uploads (criado automaticamente)
│   ├── exames_oct/         # Imagens dos exames
│   └── laudos_pdf/         # PDFs gerados
├── oct_system/              # Configurações do Django
│   ├── settings.py          # Configurações principais
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # WSGI para deploy
├── .env                     # Variáveis de ambiente (criar)
├── .venv/                   # Ambiente virtual (criar)
├── manage.py                # Gerenciador do Django
├── db.sqlite3               # Banco SQLite (criado automaticamente)
├── pyproject.toml          # Dependências do projeto
└── README.md               # Este arquivo
```

## 👥 Uso do Sistema

### 1. Primeiro Acesso
1. Execute o projeto local ou no Replit
2. Acesse o painel admin (`/admin`)
3. Configure o provedor Gemini AI
4. Cadastre o primeiro paciente
5. Envie o primeiro exame OCT

### 2. Fluxo de Trabalho
1. **Login**: Faça login no sistema
2. **Cadastrar Paciente**: Nome, data nascimento, prontuário
3. **Enviar Exame**: Selecionar paciente e upload da imagem OCT
4. **Analisar com IA**: Clique em "Analisar com IA" na página do exame
5. **Gerar Laudo**: Após análise, gere o PDF profissional

### 3. Funcionalidades por Página
- **Home**: Dashboard com resumo dos exames recentes
- **Pacientes**: Lista e cadastro de pacientes
- **Exames**: Upload e análise de imagens OCT
- **Admin**: Configuração de provedores IA e prompts

## 🔧 Configurações Avançadas

### Personalizar Visual
- Edite `static/css/style.css` para alterar cores e estilos
- Modifique templates em `core/templates/core/`

### Configurar PostgreSQL (Produção)
1. Instale o psycopg2: `pip install psycopg2-binary`
2. No `settings.py`, altere:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configurar Email (Opcional)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua_senha_de_app'
```

## 🚨 Troubleshooting

### Erro: "Chave API não configurada"
- ✅ Verifique se `GEMINI_API_KEY` está no arquivo `.env`
- ✅ Confirme se o provedor Gemini está ativo no admin
- ✅ Reinicie o servidor após alterar variáveis

### Erro: "Imagem não encontrada"
- ✅ Verifique permissões da pasta `media/`
- ✅ Confirme se o arquivo foi enviado corretamente
- ✅ Verifique se `MEDIA_URL` e `MEDIA_ROOT` estão configurados

### Erro: "Resposta vazia da API"
- ✅ Teste sua chave API no Google AI Studio
- ✅ Verifique se você tem cota/créditos disponíveis
- ✅ Confirme conectividade com a internet

### Problemas de Performance
- ✅ Use PostgreSQL em produção
- ✅ Configure cache com Redis se necessário
- ✅ Otimize imagens antes do upload

### Erro de Migração
```bash
# Resetar migrações se necessário
rm -rf core/migrations/
python manage.py makemigrations core
python manage.py migrate
```

## 📊 Monitoramento e Logs

### Ativar Logs Detalhados
No `settings.py`, adicione:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'oct_system.log',
        },
    },
    'loggers': {
        'core.ai_service': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte técnico:
- 📧 Email: suporte@seu-dominio.com
- 📱 WhatsApp: (11) 99999-9999
- 💬 Chat: Disponível no sistema

## 📚 Recursos Adicionais

- [Documentação Django](https://docs.djangoproject.com/)
- [Google Gemini AI Docs](https://ai.google.dev/docs)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.1/)
- [ReportLab Docs](https://www.reportlab.com/docs/)

---

**Sistema OCT Premium - Desenvolvido para excelência em diagnósticos médicos** ⚕️

*Versão: 1.0.0 | Última atualização: Setembro 2025*
