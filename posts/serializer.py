from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "titulo", "conteudo",
                  "autor", "categoria", "tags",
                  "status", "criado_em", "atualizado_em"]
    def min_conteudo(self, value):
        if(len(value) < 40):
            raise serializers.ValidationError("o conteudo do post deve ter no minimo 40 caracteres!")
        return value