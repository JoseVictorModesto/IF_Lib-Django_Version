from django.urls import path
from apps.notificacao.views import lista_notificacao

# urls notificações
urlpatterns = [
    path('lista_notificacao/', lista_notificacao, name='lista_notificacao'),
]