from django.db import models

# Create your models here.
class DaOrganizacao(models.Model):
    organizacao = models.ForeignKey(
        'core.Organizacao',
        on_delete=models.PROTECT)
    class Meta:
        abstract = True
class Categoria(DaOrganizacao):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome
class Tag(DaOrganizacao):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.nome


class Post(DaOrganizacao):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('revisao', 'Em revisao'),
        ('publicado', 'Publicado')
    )
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()

    autor = models.ForeignKey('core.Perfil', on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='rascunho')

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Publicacao'
        verbose_name_plural = 'Publicacoes'
        indexes = [
            models.Index(fields=['organizacao', 'criado_em'], name='posts_post_org_criado_idx'),
        ]

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f"Comentario de {self.autor} em {self.post.titulo}"
