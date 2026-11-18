from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Organizacao(models.Model):
    nome = models.CharField(max_length=120)
    criado_em = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return self.nome
    
class Perfil(models.Model):
    PAPEIS = [('admin', 'Administrador'),
    ('operador', 'Operador')]
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE)
    organizacao = models.ForeignKey(
        Organizacao, on_delete=models.PROTECT)
    papel = models.CharField(
        max_length=20, choices=PAPEIS)
    def __str__(self):
        return f'{self.usuario.username} - {self.organizacao.nome} ({self.papel})'
