from django.urls import path
from apps.notificacao.views import lista_notificacao, lista_notificacao_lida, marcar_lida, marcar_nao_lida, deletar_notificacao

# urls notificações
urlpatterns = [
    path('lista_notificacao/', lista_notificacao, name='lista_notificacao'),
    path('lista_notificacao_lida/', lista_notificacao_lida, name='lista_notificacao_lida'),
    path('marcar_lida/<int:id>', marcar_lida, name='marcar_lida'),
    path('marcar_nao_lida/<int:id>', marcar_nao_lida, name='marcar_nao_lida'),
    path('deletar_notificacao/<int:id>', deletar_notificacao, name='deletar_notificacao'),
]