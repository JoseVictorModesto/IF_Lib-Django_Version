from django.urls import path
from apps.user_admin.views import cadastro_admin, deletar_user_admin, perfil_admin, cad_campus, deletar_campus, editar_campus, editar_user_bibliotecario
from apps.user_admin.views import editar_user_admin, cad_instituicao, editar_perfil_admin, deletar_foto_admin,cad_bibliotecario
from apps.user_admin.views import deletar_instituicao, editar_instituicao, cad_curso, deletar_curso, editar_curso, deletar_bibliotecario 
from apps.user_admin.views import cad_categoria, deletar_categoria, editar_categoria, cad_tipo, deletar_tipo, editar_tipo, redefinir_senha_admin

# urls usuarios
urlpatterns = [
    # user e perfil admin
    path('cadastro_admin/', cadastro_admin, name='cadastro_admin'),
    path('perfil_admin/', perfil_admin, name='perfil_admin'),
    path('editar_perfil_admin/', editar_perfil_admin, name='editar_perfil_admin'),
    path('redefinir_senha_admin/', redefinir_senha_admin, name='redefinir_senha_admin'),
    path('deletar_foto_admin/<int:id>/', deletar_foto_admin, name='deletar_foto_admin'),
    path('deletar_user_admin/<int:id>/', deletar_user_admin, name='deletar_user_admin'),
    path('editar_user_admin/<int:id>/', editar_user_admin, name='editar_user_admin'),
    # Instituição
    path('cad_instituicao/', cad_instituicao, name='cad_instituicao'),
    path('deletar_instituicao/<int:id>/', deletar_instituicao, name='deletar_instituicao'),
    path('editar_instituicao/<int:id>/', editar_instituicao, name='editar_instituicao'),
    # Cursos
    path('cad_curso/', cad_curso, name='cad_curso'),
    path('deletar_curso/<int:id>/', deletar_curso, name='deletar_curso'),
    path('editar_curso/<int:id>/', editar_curso, name='editar_curso'),
    # Campus
    path('cad_campus/', cad_campus, name='cad_campus'),
    path('deletar_campus/<int:id>/', deletar_campus, name='deletar_campus'),
    path('editar_campus/<int:id>/', editar_campus, name='editar_campus'),
    # Categoria
    path('cad_categoria/', cad_categoria, name='cad_categoria'),
    path('deletar_categoria/<int:id>/', deletar_categoria, name='deletar_categoria'),
    path('editar_categoria/<int:id>/', editar_categoria, name='editar_categoria'),
    # Tipo
    path('cad_tipo/', cad_tipo, name='cad_tipo'),
    path('deletar_tipo/<int:id>/', deletar_tipo, name='deletar_tipo'),
    path('editar_tipo/<int:id>/', editar_tipo, name='editar_tipo'),
    # Bibliotecario
    path('cad_bibliotecario/', cad_bibliotecario, name='cad_bibliotecario'),
    path('deletar_bibliotecario/<int:id>/', deletar_bibliotecario, name='deletar_bibliotecario'),
    path('editar_user_bibliotecario/<int:id>/', editar_user_bibliotecario, name='editar_user_bibliotecario'),
]
