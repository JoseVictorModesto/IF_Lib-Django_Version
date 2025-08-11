from django.urls import path
from apps.user_aluno.views import perfil_aluno, editar_perfil_aluno, editar_foto_aluno, deletar_foto_aluno, redefinir_senha_aluno
from apps.user_aluno.views import caixa_conteudos_alunos

# urls do aluno
urlpatterns = [
    # user e perfil aluno
    path('perfil_aluno/', perfil_aluno, name='perfil_aluno'),
    path('editar_perfil_aluno/', editar_perfil_aluno, name='editar_perfil_aluno'),
    path('editar_foto_aluno/', editar_foto_aluno, name='editar_foto_aluno'),
    path('deletar_foto_aluno/<int:id>', deletar_foto_aluno, name='deletar_foto_aluno'),
    path('redefinir_senha_aluno', redefinir_senha_aluno, name='redefinir_senha_aluno'),
    # caixas de conteudos do aluno
    path('caixa_conteudos_alunos', caixa_conteudos_alunos, name='caixa_conteudos_alunos'),
]