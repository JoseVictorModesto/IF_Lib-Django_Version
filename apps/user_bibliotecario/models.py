from django.db import models

from django.contrib.auth.models import User

from apps.user_admin.models import Campus, Instituicao, Curso

class PerfilProfessor(models.Model):
    usuario = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=False, null=False, related_name='usuario_professor')
    tipo_user = models.CharField(max_length=50, default='professor')
    campus = models.ForeignKey(to=Campus, on_delete=models.SET_NULL, null=True, blank=False, related_name='professor_campus')
    instituicao = models.ForeignKey(to=Instituicao, on_delete=models.SET_NULL, null=True, blank=False, related_name='professor_instituicao')
    formacao = models.CharField(max_length=100, null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True, null=True)
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=False, related_name='professor_criador')
    
    def __str__(self):
        return self.usuario.username
    
class PerfilAluno(models.Model):
    usuario = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=False, null=False, related_name='usuario_aluno')
    tipo_user = models.CharField(max_length=50, default='aluno')
    campus = models.ForeignKey(to=Campus, on_delete=models.SET_NULL, null=True, blank=False, related_name='aluno_campus')
    instituicao = models.ForeignKey(to=Instituicao, on_delete=models.SET_NULL, null=True, blank=False, related_name='aluno_instituicao')
    curso = models.ForeignKey(to=Curso, on_delete=models.SET_NULL, null=True, blank=False, related_name='aluno_curso')
    foto_perfil = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True, null=True)
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=False, related_name='aluno_criador')

    def __str__(self):
        return self.usuario.username