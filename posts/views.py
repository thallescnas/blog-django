from django.shortcuts import render
from .models import Post

# Create your views here.
def list_posts(request):
    post_publicados = Post.objects.filter(status="publicado").order_by("-criado_em")

    return render(
        request, 'posts/list_posts.html', {
            "posts": post_publicados
        }
    )