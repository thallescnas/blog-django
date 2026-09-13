from django.contrib import admin
from .models import Categoria, Comentario, Post, Tag

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Comentario)
admin.site.register(Post)
admin.site.register(Tag)