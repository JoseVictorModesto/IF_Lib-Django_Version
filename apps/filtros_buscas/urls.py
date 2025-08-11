from django.urls import path
from apps.filtros_buscas.views import filtro_categoria, filtro_tipos, filtro_instituicao, filtro_campus, filtro_cursos, busca_principal, filtro_externos

# urls home
urlpatterns = [
    # funçao de filtros
    path('filtro_categoria/<int:id>/', filtro_categoria, name='filtro_categoria'),
    path('filtro_tipos/<int:id>/', filtro_tipos, name='filtro_tipos'),
    path('filtro_instituicao/<int:id>/', filtro_instituicao, name='filtro_instituicao'),
    path('filtro_campus/<int:id>/', filtro_campus, name='filtro_campus'),
    path('filtro_cursos/<int:id>/', filtro_cursos, name='filtro_cursos'),
    path('filtro_externos/', filtro_externos, name='filtro_externos'),
    # funçao de buscas
    path('busca_principal/', busca_principal, name='busca_principal'),
]