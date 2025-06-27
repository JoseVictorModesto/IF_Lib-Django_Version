from django.shortcuts import render, redirect
from apps.notificacao.models import Notificacao

from django.contrib import messages

def lista_notificacao(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acssar essa página!')
        return redirect('login')
    
    notificacoes = Notificacao.objects.filter(destinatario = request.user).order_by('-id')
    
    return render(request, 'notificacao/notificacoes.html', {'notificacoes':notificacoes})