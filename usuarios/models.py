from django.db import models
from django.contrib.auth.models import User

class PerfilAdmin(models.Model):
    usuario = models.OneToOneField(to=User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='img_lib/%Y/%m/%d/', blank=True, null=True)

