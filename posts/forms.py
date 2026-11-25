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


class PeriodoForm(forms.Form):
    inicio = forms.DateField(
        required=False,

    widget=forms.DateInput(attrs=
                           {"type": "date"}),
    )            
    fim = forms.DateField(
        required=False,
    widget=forms.DateInput(attrs={"type": "date"})
    )

def filtrar_periodo(request, qs):
    form = PeriodoForm(request.GET)

    if form.is_valid():
        if form.cleaned_data["inicio"]:
            qs = qs.filter(criado_em__date__gte=form.cleaned_data["inicio"])
        if form.cleaned_data["fim"]:
            qs = qs.filter(criado__emm__date__lte=form.cleaned_data["fim"])
            return qs