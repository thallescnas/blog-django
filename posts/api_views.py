from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializer import PostSerializer
from .forms import filtrar_periodo
from .dashboard import calcular_metricas

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view=None):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (hasattr(request.user, "perfil") and getattr(request.user.perfil, "papel", None) == "admin")


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(organizacao=self.request.user.perfil.organizacao)
    def perform_create(self, serializer):
        serializer.save(organizacao=self.request.user.perfil.organizacao)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(organizacao=self.request.user.perfil.organizacao)


class DashboardApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        org = request.user.perfil.organizacao
        base = filtrar_periodo(request, Post.objects.filter(organizacao=org))
        return Response(calcular_metricas(base))
