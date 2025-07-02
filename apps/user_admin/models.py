
from django.db import models
from django.contrib.auth.models import User

class PerfilAdmin(models.Model):
    # cada usuario possui um perfil
    usuario = models.OneToOneField(to=User, blank=False, null=False, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True, null=True)

class Instituicao(models.Model):
    # somente um admin é o criador da instituição, e mesmo que ele for deletado a instituição permanecerá
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name='instituicao_criada')
    nome_instituicao = models.CharField(max_length=50)
    sigla = models.CharField(max_length=20)
    estado = models.CharField(max_length=50)
    
    def __str__(self):
        return self.sigla
    
class Curso(models.Model):
    # somente um admin é o criador do curso, e mesmo que ele for deletado o curso permanecerá
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name='curso_criado')
    nome_curso = models.CharField(max_length=100)
    descricao_curso = models.TextField()

    def __str__(self):
        return self.nome_curso
    
class Campus(models.Model):
    # somente um admin é o criador do campus, e mesmo que ele for deletado o campus permanecerá
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name='campus_criado')
    nome_campus = models.CharField(max_length=100)
    email_campus = models.EmailField(max_length=100)
    endereco_campus = models.CharField(max_length=200)
    cidade_campus = models.CharField(max_length=100)
    # 1 campus pode ter somente 1 instituição, porem uma instituição pode ter varios campus, 
    # porem se a instituição for deletada todos os cursos tambem serão
    instituicao_campus = models.ForeignKey(to=Instituicao, on_delete=models.CASCADE, related_name='campus_instituicao')
    # 1 campus pode ter varios cursos, e 1 cursos pode esta varios campus
    cursos_campus = models.ManyToManyField(Curso, blank=True, related_name='campus_curso')

    def __str__(self):
        return self.nome_campus
    
class Categoria(models.Model):
    # somente um admin é o criador da categoria, e mesmo que ele for deletado a instituição categoria
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name='categoria_criado')
    nome_categoria = models.CharField(max_length=100)
    descricao_categoria = models.TextField()

    def __str__(self):
        return self.nome_categoria
    
class Tipos(models.Model):
    # somente um admin é o criador do tipo, e mesmo que ele for deletado o tipo permanecerá
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name='tipo_criado')
    nome_tipo = models.CharField(max_length=100)
    descricao_tipo = models.TextField()

    def __str__(self):
        return self.nome_tipo

class PerfilBibliotecario(models.Model):
    usuario = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=False, null=False, related_name='usuario_bibliotecario')
    tipo_user = models.CharField(max_length=50, default='bibliotecario')
    campus = models.ForeignKey(to=Campus, on_delete=models.SET_NULL, null=True, blank=False, related_name='bibliotecario_campus')
    instituicao = models.ForeignKey(to=Instituicao, on_delete=models.SET_NULL, null=True, blank=False, related_name='bibliotecario_instituicao')
    foto_perfil = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True, null=True)
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=False, related_name='bibliotecario_criador')

    def __str__(self):
        return self.usuario.username