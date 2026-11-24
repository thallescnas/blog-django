from rest_framework import generics, permissions
from .models import Post
from .serializer import PostSerializer

class isAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (hasattr(request.user, "perfil") and getattr(request.user.perfil, "papel", None) == "admin")


class PostListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, isAdminOrReadonly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(organizacao=self.request.user.perfil.organizacao)
    def perform_create(self, serializer):
        serializer.save(organizacao=self.request.user.perfil.organizacao)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, isAdminOrReadonly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(organizacao=self.request.user.perfil.organizacao)
