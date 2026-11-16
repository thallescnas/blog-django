from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "titulo", "conteudo",
                  "autor", "categoria", "tags"
                  "status", "criado_em", "atualizado_em"]