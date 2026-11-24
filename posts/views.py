from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .models import Post, Categoria
from .forms import PostForm


def org_atual(request):
    if not hasattr(request.user, 'perfil'):
        raise PermissionDenied('Este perfil não tem vinculação com Organização nenhuma.')
    return request.user.perfil.organizacao

@login_required
def list_posts(request : HttpRequest):
    org = org_atual(request)
    posts = Post.objects.filter(organizacao=org).filter(status="publicado").order_by('-criado_em')
    categorias = Categoria.objects.all()
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
        form = PostForm()
    return render(request, "posts/forms.html", {"form": form})