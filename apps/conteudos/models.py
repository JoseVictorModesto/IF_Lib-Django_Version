from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from apps.user_admin.models import Categoria, Tipos, Instituicao, Campus, Curso
from apps.user_bibliotecario.models import PerfilProfessor

from django.core.validators import FileExtensionValidator

# modelo geral de conteudos academicos
class ConteudoAcademico(models.Model):
    titulo = models.CharField(max_length=100)
    instituicao_conteudo = models.ForeignKey(to=Instituicao, on_delete=models.SET_NULL, null=True, blank=False, related_name='conteudo_instituicao')
    campus_conteudo = models.ForeignKey(to=Campus, on_delete=models.SET_NULL, null=True, blank=False, related_name='conteudo_campus')
    curso_conteudo = models.ForeignKey(to=Curso, on_delete=models.SET_NULL, null=True, blank=False, related_name='conteudo_curso')
    categoria_conteudo = models.ForeignKey(to=Categoria, on_delete=models.SET_NULL, null=True, blank=False, related_name='conteudo_categoria')
    tipos_conteudo = models.ForeignKey(to=Tipos, on_delete=models.SET_NULL, null=True, blank=False, related_name='conteudo_tipos')

    tutor_conteudo = models.ForeignKey(to=PerfilProfessor, on_delete=models.SET_NULL, null=True, blank=False, related_name='conteudo_tutor')

    descricao_conteudo = models.CharField(max_length=1500, null=False, blank=False)
    texto_conteudo = models.TextField(null=False, blank=False)

    img_capa_conteudo = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True, null=True)

    data_envio = models.DateField(default=datetime.now, null=False)

    validado = models.BooleanField(default=False)

    qtd_favoritos = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

# modelo dos autores
class Autores(models.Model):
    conteudo_cai = models.ForeignKey(to=ConteudoAcademico, on_delete=models.CASCADE, related_name='conteudo_autores')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='autor_conteudo')

# modelo das midias (imagens)
class Midias(models.Model):
    conteudo_cai = models.ForeignKey(to=ConteudoAcademico, on_delete=models.CASCADE, related_name='conteudo_midia')
    imagem_conteudo = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True ,null=True)

# modelo de conteudos adicionais
class ConteudoAdicionais(models.Model):
    conteudo_cai = models.ForeignKey(to=ConteudoAcademico, on_delete=models.CASCADE, related_name='conteudo_adicional')
    arquivo = models.FileField(upload_to='pdfs/%Y/%m/%d/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'odt', 'txt'])])

# modelo das referencias
class Referencias(models.Model):
    conteudo_cai = models.ForeignKey(to=ConteudoAcademico, on_delete=models.CASCADE, related_name='conteudo_referencia')
    referencia_conteudo = models.URLField(max_length=2000)

# modelo geral de conteudos academicos
class ConteudoExterno(models.Model):
    img_capa = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True, null=True)
    titulo = models.CharField(max_length=100)
    criador = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=False)
    campus_conteudo = models.ForeignKey(to=Campus, on_delete=models.SET_NULL, null=True, related_name='externo_campus')
    descricao_conteudo = models.TextField(null=False, blank=False)
    tipo_conteudo = models.CharField(max_length=50, default='Conteúdo Externo')
    link_conteudo = models.URLField(max_length=2000)
    data_envio = models.DateField(default=datetime.now, null=False)
    qtd_favoritos = models.IntegerField(default=0)

# modelo de caixa favoritos
class CaixaFavoritos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='user_favoritos')
    conteudo_cai = models.ManyToManyField(to=ConteudoAcademico, related_name='conteudo_favorito')

class CaixaFavoritosExternos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='user_favoritos_ex')
    conteudo_ce = models.ManyToManyField(to=ConteudoExterno, related_name='conteudo_favorito_ex')