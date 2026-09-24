from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Post, Categoria
from .forms import PostForm

def list_posts(request : HttpRequest):
    posts = Post.objects.filter(status="publicado").order_by('-criado_em')
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
def create_post(request : HttpRequest):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()
    return render(request, "posts/forms.html", {"form": form})