import csv
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .models import Post, Categoria
from .forms import PostForm, PeriodoForm, filtrar_periodo
from .dashboard import calcular_metricas


def org_atual(request):
    if not hasattr(request.user, 'perfil'):
        raise PermissionDenied('Este perfil não tem vinculação com Organização nenhuma.')
    return request.user.perfil.organizacao

def isadmin(user):
    return hasattr(user, 'perfil') and getattr(user.perfil, "papel", None) == 'admin'

@login_required
def list_posts(request : HttpRequest):
    org = org_atual(request)
    posts = (
        Post.objects.filter(organizacao=org, status="publicado")
        .select_related("autor__usuario", "categoria")
        .order_by('-criado_em')
    )
    categorias = Categoria.objects.filter(organizacao=org)
    q = request.GET.get('q', '')
    categoria = request.GET.get('categorias', '')
    
    if q:
        posts = posts.filter(Q(titulo__icontains=q))
    if categoria:
        posts = posts.filter(categoria__nome=categoria)
    return render(request, 'posts/list_posts.html', {
        "posts": posts,
        "categorias": categorias
    })
@login_required
def create_post(request : HttpRequest):

    if not isadmin(request.user):
        raise PermissionDenied("Apenas os adm podem fazer postagens!")
    org = org_atual(request)
    if request.method == "POST":
        form = PostForm(request.POST or None, org=org)
        if form.is_valid():
            post = form.save(commit=False)
            post.organizacao = org
            post.save()
            form.save_m2m()
            return redirect("posts")
    else:
        form = PostForm(org=org)
    return render(request, "posts/forms.html", {"form": form})

@login_required
def dashboard(request: HttpRequest):
    org = org_atual(request)
    base = filtrar_periodo(request, Post.objects.filter(organizacao=org))

    metricas = calcular_metricas(base)

    contexto = {
        **metricas,
        "form": PeriodoForm(request.GET),
        "organizacao": org,
        "mostra_series": isadmin(request.user),
    }
    return render(request, "posts/dashboard.html", contexto)


def _sanitizar_csv(valor):
    texto = str(valor or "")
    if texto.startswith(("=", "+", "-", "@")):
        return "'" + texto
    return texto


@login_required
def exportar_csv(request: HttpRequest):
    org = org_atual(request)
    if not isadmin(request.user):
        raise PermissionDenied("Apenas administradores podem exportar o relatório.")

    qs = filtrar_periodo(
        request,
        Post.objects.filter(organizacao=org)
        .select_related("autor__usuario", "categoria")
        .order_by("-criado_em"),
    )

    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = 'attachment; filename="posts.csv"'
    writer = csv.writer(resp)
    writer.writerow(["Título", "Autor", "Categoria", "Status", "Criado em"])

    for post in qs:
        writer.writerow([
            _sanitizar_csv(post.titulo),
            _sanitizar_csv(post.autor.usuario.username),
            _sanitizar_csv(post.categoria.nome if post.categoria else ""),
            post.get_status_display(),
            post.criado_em.strftime("%d/%m/%Y %H:%M"),
        ])
    return resp