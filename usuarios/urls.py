from django.urls import path
from usuarios.views import login, cadastro_admin, logout, deletar_user_admin, perfil_admin, editar_user_admin, cad_instituicao, editar_perfil, deletar_foto_perfil

# urls usuarios
urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro_admin/', cadastro_admin, name='cadastro_admin'),
    path('perfil_admin/', perfil_admin, name='perfil_admin'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('deletar_foto_perfil/<int:id>/', deletar_foto_perfil, name='deletar_foto_perfil'),
    path('logout/', logout, name='logout'),
    path('deletar_user_admin/<int:id>/', deletar_user_admin, name='deletar_user_admin'),
    path('editar_user_admin/<int:id>/', editar_user_admin, name='editar_user_admin'),
    path('cad_instituicao/', cad_instituicao, name='cad_instituicao'),
]