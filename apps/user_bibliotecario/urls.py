from django.urls import path
from apps.user_bibliotecario.views import informacoes_bibliotecario, editar_perfil_bibliotecario, editar_foto_bibliotecario, deletar_foto_bibliotecario, redefinir_senha_bibliotecario
from apps.user_bibliotecario.views import cad_professor, deletar_professor, editar_professor
from apps.user_bibliotecario.views import cad_aluno, deletar_aluno, editar_aluno
# urls bibliotecario
urlpatterns = [
    # user e perfil bibliotecario
    path('informacoes_bibliotecario/', informacoes_bibliotecario, name='informacoes_bibliotecario'),
    path('editar_perfil_bibliotecario/', editar_perfil_bibliotecario, name='editar_perfil_bibliotecario'),
    path('editar_foto_bibliotecario/', editar_foto_bibliotecario, name='editar_foto_bibliotecario'),    
    path('deletar_foto_bibliotecario/<int:id>/', deletar_foto_bibliotecario, name='deletar_foto_bibliotecario'),    
    path('redefinir_senha_bibliotecario/', redefinir_senha_bibliotecario, name='redefinir_senha_bibliotecario'),
    # professores
    path('cad_professor/', cad_professor, name='cad_professor'),
    path('deletar_professor/<int:id>/', deletar_professor, name='deletar_professor'),  
    path('editar_professor/<int:id>/', editar_professor, name='editar_professor'),    
    # alunos
    path('cad_aluno/', cad_aluno, name='cad_aluno'),
    path('deletar_aluno/<int:id>/', deletar_aluno, name='deletar_aluno'),
    path('editar_aluno/<int:id>/', editar_aluno, name='editar_aluno'), 
]