from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Organizacao(models.Model):
    nome = models.CharField(max_length=120)
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
class Tag(models.Model):
    nome = models.CharField(max_length=100)

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
class Post(models.Model):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('revisao', 'Em revisão'),
        ('publicado', 'Publicado')
    )
    organizacao = models.ForeignKey(
        Organizacao
        , on_delete=models.PROTECT
    )
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()

    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='rascunho')

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.post.titulo}"
