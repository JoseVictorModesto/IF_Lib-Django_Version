from django.shortcuts import render, redirect
from apps.notificacao.models import Notificacao

from django.contrib import messages

def lista_notificacao(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acssar essa página!')
        return redirect('login')
    
    notificacoes = Notificacao.objects.filter(destinatario = request.user).order_by('-id')
    
    return render(request, 'notificacao/notificacoes.html', {'notificacoes':notificacoes})

def notificacao_bemvindo(request, destinatario):
    notificacao = Notificacao.objects.create(
        remetente = request.user,
        destinatario = destinatario,
        titulo_notificacao = 'Bem vindo ao IF_Lib',
        descricao_notificacao = f'Olá {destinatario.first_name}, seja muito bem vindo(a) ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!',
    )

    return notificacao