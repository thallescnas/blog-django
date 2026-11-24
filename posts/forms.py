from core.models import Perfil
from django import forms
from .models import Post, Tag, Categoria

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'categoria', 'tags', 'autor']

        def __init__(self, *args, org=None, **kwargs):
            super().__init__(*args, **kwargs)
            if org:
                self.fields['categoria'].queryset = Categoria.objects.filter(
                organizacao=org)
                self.fields['tags'].queryset = Tag.objects.filter(organizacao=org)
                self.fields['autor'].queryset = Perfil.objects.filter(
                    organizacao=org)
    def clean_conteudo(self):
        conteudo = self.cleaned_data.get("conteudo")
        if conteudo and len(conteudo.strip()) < 50:
            raise forms.ValidationError(f'O conteudo deve ter no minomo 50 caracteres.'
                                        f'Você tem apenas {len(conteudo.strip())}')            