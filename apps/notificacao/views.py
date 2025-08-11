from django.shortcuts import render, redirect, get_object_or_404
from apps.notificacao.models import Notificacao

from django.contrib import messages

from django.views.decorators.http import require_http_methods, require_POST

from apps.login_perfil.views import deletar_obj

from django.contrib.auth.models import User



def notificacao_bemvindo(request, destinatario):
    notificacao = Notificacao.objects.create(
        remetente = request.user,
        destinatario = destinatario,
        titulo_notificacao = 'Bem vindo ao IF_Lib',
        descricao_notificacao = f'Olá {destinatario.first_name}, seja muito bem vindo(a) ao IF_Lib, venha conosco descobrir um universo de conhecimento. Estamos felizes em ter você com a gente. Boa jornada!!',
    )

    return notificacao

def notificacao(request, destinatario_not, conteudo_not, titulo_not, descricao_not):
    notificacao = Notificacao.objects.create(
        remetente = request.user,
        destinatario = destinatario_not,
        conteudo = conteudo_not,
        titulo_notificacao = titulo_not,
        descricao_notificacao = descricao_not
    )
    return notificacao

def status_notificacao(request, id, stts, mensagem):
    if request.method == 'POST':
        notificacao = get_object_or_404(Notificacao, id=id, destinatario=request.user)
        notificacao.lida = stts
        notificacao.save()
        messages.success(request, mensagem)

def verificar_auth(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para acessar essa página!')
        return redirect('login')
    
# --------------------------------------------------------------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def lista_notificacao(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth

    notificacoes = Notificacao.objects.filter(destinatario = request.user, lida=False).order_by('-id')

    return render(request, 'notificacao/notificacoes.html', {'notificacoes':notificacoes})

@require_POST
def marcar_lida(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    status_notificacao(request, id, True, 'Notificação marcada como lida')
    return redirect('lista_notificacao')

# --------------------------------------------------------------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def lista_notificacao_lida(request):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    notificacoes = Notificacao.objects.filter(destinatario = request.user, lida=True).order_by('-id')

    return render(request, 'notificacao/notificacoes_lidas.html', {'notificacoes':notificacoes})

@require_POST
def marcar_nao_lida(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    status_notificacao(request, id, False, 'Notificação marcada como não lida')
    return redirect('lista_notificacao_lida')

@require_POST
def deletar_notificacao(request, id):
    usuario_auth = verificar_auth(request)
    if usuario_auth:
        return usuario_auth
    
    notificacao = get_object_or_404(Notificacao, id=id)

    if notificacao.destinatario != request.user:
        messages.error(request, 'Você não pode deletar a notificação de outro usuário.')
        return redirect('home')
    
    if request.method == 'POST':
        deletar_obj(request, Notificacao, 'Notificação deletada com sucesso!', id)
        return redirect('lista_notificacao_lida')



