from django.db import models
from django.contrib.auth.models import User
from apps.conteudos.models import ConteudoAcademico

class Notificacao(models.Model):
    remetente = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='notificacao_remetente')
    destinatario = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='notificacao_destinatario')
    conteudo = models.ForeignKey(to=ConteudoAcademico, on_delete=models.CASCADE, null=True, blank=True)
    titulo_notificacao = models.CharField(max_length=300, null=False)
    descricao_notificacao = models.TextField(null=False)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo_notificacao