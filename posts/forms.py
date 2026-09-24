from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'categoria', 'tags', 'autor']
    def clean_conteudo(self):
        conteudo = self.cleaned_data.get("conteudo")
        
        if conteudo and len(conteudo.strip()) < 50:
            raise forms.ValidationError(f'O conteudo deve ter no minomo 50 caracteres.'
                                        f'Você tem apenas {len(conteudo.strip())}')            