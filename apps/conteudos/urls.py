from django.urls import path
from apps.conteudos.views import cad_cai, vizualizar_cai, vizualizar_cai_nao_valid, validar_cai, revisao_cai, editar_cai, salvar_favorito, remover_favorito, todos_favorito, cad_externo, vizualizar_ce
from apps.conteudos.views import editar_externo, salvar_favorito_ex, remover_favorito_ex, todos_favorito_ex

urlpatterns = [
    path('cad_cai/', cad_cai, name='cad_cai'),
    path('vizualizar_cai/<int:id>', vizualizar_cai, name='vizualizar_cai'),
    path('vizualizar_cai_nao_valid/<int:id>', vizualizar_cai_nao_valid, name='vizualizar_cai_nao_valid'),
    path('validar_cai/<int:id>', validar_cai, name='validar_cai'),
    path('revisao_cai/<int:id>', revisao_cai, name='revisao_cai'),
    path('editar_cai/<int:id>', editar_cai, name='editar_cai'),
    path('salvar_favorito/<int:id>', salvar_favorito, name='salvar_favorito'),
    path('remover_favorito/<int:id>', remover_favorito, name='remover_favorito'),
    path('todos_favorito/', todos_favorito, name='todos_favorito'),
    path('cad_externo/', cad_externo, name='cad_externo'),
    path('vizualizar_ce/<int:id>', vizualizar_ce, name='vizualizar_ce'),
    path('editar_externo/<int:id>', editar_externo, name='editar_externo'),
    path('salvar_favorito_ex/<int:id>', salvar_favorito_ex, name='salvar_favorito_ex'),
    path('remover_favorito_ex/<int:id>', remover_favorito_ex, name='remover_favorito_ex'),
    path('todos_favorito_ex/', todos_favorito_ex, name='todos_favorito_ex'),
]
