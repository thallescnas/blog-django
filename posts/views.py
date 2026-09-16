from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Create your views here.
def list_posts(request):
    post_publicados = Post.objects.filter(status="publicado").order_by("-criado_em")

    return render(
        request, 'posts/list_posts.html', {
            "posts": post_publicados
        }
    )

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()
    return render(request, "posts/forms.html", {"form": form})