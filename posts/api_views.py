from rest_framework import generics, permissions
from .models import Post
from .serializer import PostSerializer

class isAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (hasattr(request.user, "perfil") and getattr(request.user.perfil, "papel", None) == "admin")


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer