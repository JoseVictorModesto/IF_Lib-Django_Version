from django.db import models
from django.contrib.auth.models import User

class Notificacao(models.Model):
    remetente = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='notificacao_remetente')
    destinatario = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='notificacao_destinatario')
    titulo_notificacao = models.CharField(max_length=100, null=False)
    descricao_notificacao = models.TextField(null=False)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo_notificacao
    
