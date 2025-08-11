from django.urls import path
from apps.user_professor.views import perfil_professor, editar_perfil_professor, editar_foto_professor, deletar_foto_professor, redefinir_senha_professor
from apps.user_professor.views import caixa_conteudos_professor, caixa_conteudos_validar_professor, caixa_conteudos_externos
# urls do professor
urlpatterns = [
    # user e perfil professor
    path('perfil_professor/', perfil_professor, name='perfil_professor'),
    path('editar_perfil_professor/', editar_perfil_professor, name='editar_perfil_professor'),
    path('editar_foto_professor/', editar_foto_professor, name='editar_foto_professor'),
    path('deletar_foto_professor/<int:id>/', deletar_foto_professor, name='deletar_foto_professor'),    
    path('redefinir_senha_professor/', redefinir_senha_professor, name='redefinir_senha_professor'),    
    # caixas de conteudos do aluno
    path('caixa_conteudos_professor/', caixa_conteudos_professor, name='caixa_conteudos_professor'), 
    path('caixa_conteudos_validar_professor/', caixa_conteudos_validar_professor, name='caixa_conteudos_validar_professor'), 
    path('caixa_conteudos_externos/', caixa_conteudos_externos, name='caixa_conteudos_externos'), 
]