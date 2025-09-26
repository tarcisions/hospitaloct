from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/novo/', views.paciente_create, name='paciente_create'),
    path('exames/novo/', views.exame_create, name='exame_create'),
    path('exames/<int:exame_id>/', views.exame_analyze, name='exame_analyze'),
    path('exames/<int:exame_id>/analise-ia/', views.exame_analyze_ai, name='exame_analyze_ai'),
    path('api/check-gemini-key/', views.check_gemini_key, name='check_gemini_key'),
    path('exames/<int:exame_id>/gerar-laudo-pdf/', views.gerar_laudo_pdf_view, name='gerar_laudo_pdf'),
]